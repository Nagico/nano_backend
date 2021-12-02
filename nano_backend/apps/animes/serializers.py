from rest_framework import serializers

import users.models
from nano_backend.utils.serializers import LimitedListSerializer
from photos.serializers import PhotoLimitSerializer
from places.serializers import PlaceLimitSerializer
from .models import Anime


class AnimeDetailSerializer(serializers.ModelSerializer):
    """
    Anime 详细序列化器
    """
    places = PlaceLimitSerializer(label='地点预览', many=True, read_only=True)
    photos = PhotoLimitSerializer(label='图片预览', many=True, read_only=True)

    class Meta:
        model = Anime
        fields = '__all__'

        read_only_fields = ['place', 'create_user', 'contributor', 'is_approved', 'collection_num']

    def validate(self, attrs):
        """
        添加创建者信息
        """
        attrs['create_user'] = self.context['request'].user
        attrs['contributor'] = [self.context['request'].user]

        return attrs


class AnimeInfoSerializer(serializers.ModelSerializer):
    """
    Anime 简要序列化器
    """
    class Meta:
        model = Anime
        fields = ['id', 'title', 'title_cn', 'cover', 'cover_small']


class AnimeLimitSerializer(serializers.ModelSerializer):
    """
    anime 带约束序列化器
    """
    class Meta:
        list_serializer_class = LimitedListSerializer
        model = Anime
        fields = ['id', 'title', 'title_cn', 'cover', 'cover_small']
