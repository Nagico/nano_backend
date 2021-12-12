from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from nano_backend.utils.serializers import LimitedListSerializer
from photos.serializers import PhotoLimitSerializer
from places.serializers import PlaceLimitSerializer
from staffs.serializers import StaffInfoSerializer
from tags.serializers import TagSerializer
from users.models import UserAnimeCollection
from .models import Anime


class AnimeInfoSerializer(serializers.ModelSerializer):
    """
    Anime 简要序列化器
    """
    is_collected = serializers.SerializerMethodField(label='是否收藏')

    class Meta:
        model = Anime
        fields = ['id', 'title_cn', 'cover_medium', 'is_collected']

    def get_is_collected(self, obj):
        """
        是否收藏
        """
        try:
            user = self.context['request'].user  # 获取当前用户
        except:  # 无request信息
            return False
        if not user.is_authenticated:  # 当前用户未登录
            return False
        anime = obj
        if UserAnimeCollection.objects.filter(user=user, anime=anime).exists():
            return True
        return False


class AnimeDetailSerializer(AnimeInfoSerializer):
    """
    Anime 详细序列化器
    """
    places = PlaceLimitSerializer(label='地点预览', many=True, read_only=True)
    photos = PhotoLimitSerializer(label='图片预览', many=True, read_only=True)
    alias = StringRelatedField(label='别名', many=True, read_only=True)
    director = StaffInfoSerializer(label='导演', many=True, read_only=True)
    original = StaffInfoSerializer(label='原作', many=True, read_only=True)
    script = StaffInfoSerializer(label='脚本', many=True, read_only=True)
    storyboard = StaffInfoSerializer(label='分镜', many=True, read_only=True)
    actor = StaffInfoSerializer(label='演出', many=True, read_only=True)
    music = StaffInfoSerializer(label='音乐', many=True, read_only=True)
    producer = StaffInfoSerializer(label='动画制作', many=True, read_only=True)
    tags = TagSerializer(label='标签', many=True, read_only=True)

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


class AnimeLimitSerializer(serializers.ModelSerializer):
    """
    anime 带约束序列化器
    """
    class Meta:
        list_serializer_class = LimitedListSerializer
        model = Anime
        fields = ['id', 'title', 'title_cn', 'cover', 'cover_small']
