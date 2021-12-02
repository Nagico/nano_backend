from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ListSerializer

import users.models
from nano_backend.utils.serializers import LimitedListSerializer
from photos.serializers import PhotoLimitSerializer
from .models import Place


class PlaceDetailsSerializer(ModelSerializer):
    """
    place 详细信息
    """
    photos = PhotoLimitSerializer(label='图片预览', many=True, read_only=True)  # 嵌套序列化器

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


class PlaceInfoSerializer(ModelSerializer):
    """
    place 简要信息
    """
    class Meta:
        model = Place
        fields = ['id', 'name', 'address']


class PlaceLimitSerializer(ModelSerializer):
    """
    place 带约束序列化器
    """
    class Meta:
        list_serializer_class = LimitedListSerializer
        model = Place
        fields = ['id', 'name']
