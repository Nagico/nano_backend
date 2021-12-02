from rest_framework.serializers import ModelSerializer, ListSerializer

import users.models
from nano_backend.utils.serializers import LimitedListSerializer
from photos.serializers import PhotoLimitSerializer
from .models import Place


class PlaceDetailsSerializer(ModelSerializer):
    """
    place 详细信息
    """
    photos = PhotoLimitSerializer(many=True, read_only=True)

    class Meta:
        model = Place
        fields = '__all__'
        read_only_fields = ['photo', 'create_user', 'contributor', 'is_approved']

    def validate(self, attrs):
        # attrs['create_user'] = self.context['request'].user
        # attrs['contributor'] = self.context['request'].user
        attrs['create_user'] = users.models.User.objects.get(pk=1)
        attrs['contributor'] = [users.models.User.objects.get(pk=1)]
        return attrs


class PlaceInfoSerializer(ModelSerializer):
    """
    place 简要信息
    """
    class Meta:
        model = Place
        fields = ['id', 'name']


class PlaceLimitSerializer(ModelSerializer):
    """
    place 带约束序列化器
    """
    class Meta:
        list_serializer_class = LimitedListSerializer
        model = Place
        fields = ['id', 'name']
