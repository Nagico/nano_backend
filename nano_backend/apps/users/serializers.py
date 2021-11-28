from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import User


class UserInfoSerializer(ModelSerializer):
    """
    用户信息序列化器（所有信息）
    """
    class Meta:
        model = User
        exclude = ['password', 'is_active', 'is_superuser', 'is_staff', 'date_joined', 'last_login']

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


class UserIntentionSerializer(ModelSerializer):
    """
    用户求职意向序列化器
    """

    class Meta:
        model = UserInfo
        fields = ['uid', 'intention']
