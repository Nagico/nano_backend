from rest_framework import serializers

from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Tag 简要序列化器
    """
    class Meta:
        model = Tag
        fields = ['id', 'name']

