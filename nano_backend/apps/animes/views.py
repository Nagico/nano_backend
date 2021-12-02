from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q

from users.models import User
from .filters import AnimeFilter
from .models import Anime
from .serializers import AnimeSerializer


class AnimeViewSet(ModelViewSet):
    """
    Anime ViewSet
    """
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]  # 排序 过滤

    ordering_fields = ['id', 'create_time', 'update_time', 'title', 'title_cn', 'is_approved', 'is_public',
                       'create_user', 'anime_id']  # 排序字段
    filterset_class = AnimeFilter  # 自定义过滤器

    def get_queryset(self):
        return self.queryset.filter(Q(is_approved=True) | Q(create_user=User.objects.get(pk=1)))

    def update(self, request, *args, **kwargs):
        """
        支持部分更新
        """
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

