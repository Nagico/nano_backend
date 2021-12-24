from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from recommendation.models import Recommendation
from recommendation.serializers import RecommendationSerializer


class RecommendationViewSet(ModelViewSet):
    """
    Reco ViewSet
    """
    serializer_class = RecommendationSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]  # 排序 过滤
    queryset = Recommendation.objects.all()

    ordering_fields = ['score', 'create_time', 'update_time', 'id']  # 排序字段
    ordering = ['-score']  # 默认排序字段
    filter_fields = ['type']

    permission_classes = [AllowAny]  # 允许任何人
