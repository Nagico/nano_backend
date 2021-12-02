from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from users.models import User
from .models import Photo
from .serializers import PhotoDetailSerializer


class PhotoViewSet(ModelViewSet):
    queryset = Photo.objects.filter(Q(is_approved=True) | Q(create_user=User.objects.get(pk=1)))
    filter_backends = [OrderingFilter, DjangoFilterBackend]  # 排序 过滤
    serializer_class = PhotoDetailSerializer

    ordering_fields = ['id', 'create_time', 'update_time', 'is_approved', 'is_public', 'anime_id', 'place_id', 'create_user']  # 排序
    filter_fields = ['id', 'is_approved', 'is_public', 'anime_id', 'place_id', 'create_user']  # 过滤

    def update(self, request, *args, **kwargs):
        """
        支持部分更新
        """
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
