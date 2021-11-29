from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import PasswordField, TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from .models import User
from nano_backend.utils.crypto import Crypto


class UserSerializer(ModelSerializer):
    """
    用户信息序列化器（所有信息）
    """
    class Meta:
        model = User
        exclude = ['is_active', 'is_superuser', 'is_staff', 'date_joined', 'last_login',
                   'first_name', 'last_name', 'groups', 'user_permissions']

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
        # rsa 解密
        c = Crypto()
        password = c.decrypt(attrs['password'])
        password2 = c.decrypt(attrs['password2'])

        if password != password2:
            raise serializers.ValidationError(detail='Password does not match', code='password_not_match')

        attrs['password'] = make_password(password)
        attrs.pop('password2')  # 删除密码2

        return attrs


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