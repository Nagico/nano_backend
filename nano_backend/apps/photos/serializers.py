from rest_framework.serializers import ModelSerializer, ListSerializer

import users.models
from nano_backend.utils.choices import StatusChoice
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
        # attrs['create_user'] = self.context['request'].user
        attrs['create_user'] = users.models.User.objects.get(pk=1)
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
