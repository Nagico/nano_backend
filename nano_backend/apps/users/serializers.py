import re

from django.contrib.auth.hashers import make_password
from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField, TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from nano_backend.utils.crypto import Crypto


class UserSerializer(serializers.ModelSerializer):
    """
    用户信息序列化器（所有信息）
    """
    class Meta:
        model = User
        exclude = ['is_active', 'is_superuser', 'is_staff', 'date_joined', 'last_login',
                   'first_name', 'last_name', 'groups', 'user_permissions', 'email']

    password = PasswordField(write_only=True)
    password2 = PasswordField(write_only=True)

    def validate_avatar(self, value):
        """
        头像检测
        """
        if not value:  # 未找到头像文件
            return 'media/avatar/default.jpg'

        if value.content_type not in ['image/jpeg', 'image/png', 'image/gif']:  # 文件类型不正确
            raise serializers.ValidationError(detail='Avatar is not a image', code='avatar_not_image')

        if value.size > 1024 * 1024 * 2:  # 头像文件大于2M
            raise serializers.ValidationError(detail='Avatar is larger than 2MB', code='avatar_too_large')
        if value.size < 1024:  # 头像文件小于1KB
            raise serializers.ValidationError(detail='Avatar is smaller than 1KB', code='avatar_too_small')

        if self.instance.avatar != 'media/avatar/default.jpg':  # 已存在头像文件
            self.instance.avatar.delete()  # 删除原头像文件

        return value

    def validate(self, attrs):
        """
        联合校验密码
        :param attrs:
        :return:
        """
        if hasattr(attrs, 'password') and hasattr(attrs, 'password2'):
            # rsa 解密
            c = Crypto()
            password = c.decrypt(attrs['password'])
            password2 = c.decrypt(attrs['password2'])

            if password != password2:
                raise serializers.ValidationError(detail='Password does not match', code='password_not_match')

            attrs['password'] = make_password(password)
            attrs.pop('password2')  # 删除密码2

        return attrs


class UserInfoSerializer(serializers.ModelSerializer):
    """
    公开信息序列化器
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar']


class LoginTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    登录获取token序列化器
    """
    def validate_password(self, value):
        """
        rsa 解密
        """
        c = Crypto()
        return c.decrypt(value)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['id'] = self.user.id
        data['username'] = self.user.username
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class CreateUserSerializer(serializers.ModelSerializer):
    """
    注册序列化器
    """

    # 序列化器的所有字段 ['id', 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow']
    # 校验字段 ['username', 'password', 'password2', 'mobile', 'sms_code', 'allow']
    # 已存在字段 ['id', 'username', 'password', 'mobile']

    # 需要序列化（后端响应）的字段 ['id', 'username', 'mobile', 'token]
    # 需要反序列化（前端返回）的字段 ['username', 'password', 'password2', 'mobile', 'sms_code', 'allow']  write_only=True

    password = PasswordField(label='密码', write_only=True)
    password2 = PasswordField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    allow = serializers.CharField(label='同意协议', write_only=True)  # 传回 'true'
    refresh = serializers.CharField(label='刷新令牌', read_only=True)  # JWT
    access = serializers.CharField(label='访问令牌', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow', 'refresh',
                  'access']  # 序列化器内容
        extra_kwargs = {  # 简易校验字段
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {  # 自定义校验信息
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            }
        }

    def validate_mobile(self, value):
        """
        手机号校验
        """
        if not re.match(r'1[3-9]\d{9}', value):
            raise serializers.ValidationError('手机号格式错误', code='mobile_invalid')

        return value

    def validate_allow(self, value):
        """
        同意协议
        """
        if value != 'true':
            raise serializers.ValidationError('请同意用户协议', code='allow_invalid')

        return value

    def validate(self, attrs):
        """
        校验密码与短信校验码
        """
        # 判断两次密码是否一致
        c = Crypto()
        attrs['password'] = c.decrypt(attrs['password'])
        attrs['password2'] = c.decrypt(attrs['password2'])
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两个密码不一致', code='password_not_match')

        if not 8 <= len(attrs['password']) <= 20:
            raise serializers.ValidationError('仅允许8-20个字符的密码', code='password_length_invalid')

        # 判断短信验证码是否正确
        redis_conn = get_redis_connection('verify_codes')
        mobile = attrs['mobile']

        real_sms_code = redis_conn.get(f'sms_{mobile}')
        # redis中取出是bytes类型，需要转换成str
        if real_sms_code is None or real_sms_code.decode() != attrs['sms_code']:
            raise serializers.ValidationError('短信验证码错误', code='sms_code_invalid')

        return attrs

    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create(self, validated_data):
        """
        创建用户, 追加返回 jwt token
        """
        # 删除数据库中不需要的字段
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        password = validated_data.pop('password')  # 避免密码明文存储

        # 创建用户
        user = User(**validated_data)
        user.set_password(password)  # 密码加密
        user.save()

        # 生成jwt token
        token = CreateUserSerializer.get_tokens_for_user(user)
        user.refresh = token['refresh']
        user.access = token['access']

        return user
