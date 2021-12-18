from django.db.models import Q
from rest_framework.serializers import ModelSerializer

from nano_backend.utils.choices import ImageTypeChoice
from nano_backend.utils.serializers import LimitedListSerializer
from .models import Photo


class PhotoDetailSerializer(ModelSerializer):
    """
    photo 详细信息
    """
    class Meta:
        model = Photo
        fields = '__all__'
        read_only_fields = ['create_user', 'is_approved']

    def validate(self, attrs):
        attrs['create_user'] = self.context['request'].user  # 获取当前登录用户
        return attrs


class PhotoInfoSerializer(ModelSerializer):
    """
    photo 简要信息
    """
    class Meta:
        model = Photo
        fields = ['id', 'name', 'image']


class PhotoLimitSerializer(ModelSerializer):
    """
    photo 带约束序列化器
    """
    class Meta:
        list_serializer_class = LimitedListSerializer
        model = Photo
        fields = ['id', 'name', 'image']

    def get_queryset(self):
        return Photo.objects.filter(type=ImageTypeChoice.REAL)


