from rest_framework import serializers

from nano_backend.utils.serializers import LimitedListSerializer
from photos.serializers import PhotoLimitSerializer
from places.serializers import PlaceLimitSerializer
from users.models import UserAnimeCollection
from .models import Anime


class AnimeDetailSerializer(serializers.ModelSerializer):
    """
    Anime 详细序列化器
    """
    places = PlaceLimitSerializer(label='地点预览', many=True, read_only=True)
    photos = PhotoLimitSerializer(label='图片预览', many=True, read_only=True)
    is_collected = serializers.SerializerMethodField(label='是否收藏')

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

    def get_is_collected(self, obj):
        """
        是否收藏
        """
        user = self.context['request'].user  # 获取当前用户
        if not user.is_authenticated:  # 当前用户未登录
            return False
        anime = self.instance
        if UserAnimeCollection.objects.filter(user=user, anime=anime).exists():
            return True
        return False


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
