from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from users.models import User
from .filters import PlaceFilter
from .models import Place
from .serializers import PlaceDetailsSerializer


class PlaceViewSet(ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceDetailsSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]  # 排序 过滤

    ordering_fields = ['id', 'create_time', 'update_time', 'name', 'is_approved', 'is_public', 'create_user', 'anime_id']  # 排序字段
    filterset_class = PlaceFilter  # 自定义过滤器

    def update(self, request, *args, **kwargs):
        """
        支持部分更新
        """
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        return self.queryset.filter(Q(is_approved=True) | Q(create_user=User.objects.get(pk=1)))

