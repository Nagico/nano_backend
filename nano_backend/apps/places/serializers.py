from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ListSerializer

from users.models import UserPlaceCollection
from nano_backend.utils.serializers import LimitedListSerializer
from photos.serializers import PhotoLimitSerializer
from .models import Place


class PlaceDetailsSerializer(ModelSerializer):
    """
    place 详细信息
    """
    photos = PhotoLimitSerializer(label='图片预览', many=True, read_only=True)  # 嵌套序列化器
    is_collected = serializers.SerializerMethodField(label='是否收藏')

    class Meta:
        model = Place
        fields = '__all__'
        read_only_fields = ['photo', 'create_user', 'contributor', 'is_approved', 'collection_num']

    def validate(self, attrs):
        """
        自动添加创建者信息
        """
        attrs['create_user'] = self.context['request'].user
        attrs['contributor'] = [self.context['request'].user]
        return attrs

    def get_is_collected(self, obj):
        """
        是否收藏
        """
        user = self.context['request'].user  # 获取当前用户
        if not user.is_authenticated:  # 当前用户未登录
            return False
        place = obj
        if UserPlaceCollection.objects.filter(user=user, place=place).exists():
            return True
        return False

class PlaceInfoSerializer(ModelSerializer):
    """
    place 简要信息
    """
    class Meta:
        model = Place
        fields = ['id', 'name', 'city', 'address']


class PlaceLimitSerializer(ModelSerializer):
    """
    place 带约束序列化器
    """
    class Meta:
        list_serializer_class = LimitedListSerializer
        model = Place
        fields = ['id', 'name']
