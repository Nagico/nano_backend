from rest_framework import serializers

from tags.serializers import TagSerializer
from .models import Recommendation


class RecommendationSerializer(serializers.ModelSerializer):
    """
    序列化器
    """

    tags = TagSerializer(label='标签', many=True, read_only=True)

    class Meta:
        model = Recommendation
        fields = '__all__'
