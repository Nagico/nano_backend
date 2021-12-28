import logging
from django.conf import settings

from django.db.models import Q
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from animes.models import Anime
from nano_backend.utils.auth import check_permission
from nano_backend.utils.mixins.views import CacheListModelMixin, CacheRetrieveModelMixin
from places.models import Place
from users.models import User
from .models import Photo
from .serializers import PhotoDetailSerializer

logger = logging.getLogger(__name__)

CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 60 * 1)


class PhotoViewSet(CacheListModelMixin, CacheRetrieveModelMixin, ModelViewSet):
    queryset = Photo.objects.filter(is_public=True, is_approved=True)
    filter_backends = [OrderingFilter, DjangoFilterBackend]  # 排序 过滤
    serializer_class = PhotoDetailSerializer

    ordering_fields = ['id', 'create_time', 'update_time', 'is_approved', 'is_public', 'anime_id', 'place_id',
                       'create_user']  # 排序
    filter_fields = ['id', 'is_approved', 'is_public', 'anime_id', 'place_id', 'create_user']  # 过滤

    permission_classes = [AllowAny]  # 允许任何人

    def create(self, request, *args, **kwargs):
        """
        创建照片
        """
        check_permission(self)

        logger.info(f'[photo/] user {self.request.user} create: {request.data}')
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        更新照片
        """

        check_permission(self)

        kwargs['partial'] = True
        logger.info(f'[photo/{self.kwargs["pk"]}/] user {self.request.user} update: {request.data}')
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        instance = self.get_object()
        if 'image' in serializer.validated_data:  # 删除旧图片
            instance.image.delete()
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """
        删除照片
        """
        check_permission(self)

        logger.info(f'[photo/{self.kwargs["pk"]}/] user {self.request.user} destroy')
        return super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        """
        删除时删除图片
        """
        instance.image.delete()
        instance.delete()

    def update_contributor(self):
        """
        更新贡献者
        :return:
        """
        anime = None
        place = None
        if self.action == 'create':  # 创建
            if self.request.data.get('is_public', False) is True:  # 已公开
                # 从请求中获取id
                anime = Anime.objects.get(pk=self.request.data['anime_id'])
                place = Place.objects.get(pk=self.request.data['place_id'])
        elif self.action == 'update':  # 更新
            if self.request.data.get('is_public', False) is True:  # 已公开
                # 从数据库中查询
                photo = Photo.objects.get(pk=self.kwargs['pk'])
                anime = photo.anime_id
                place = photo.place_id
        if anime and place:  # 更新贡献者
            anime.contributor.add(self.request.user)
            place.contributor.add(self.request.user)
            logger.info(f'[anime/{anime.id}/] add contributor: {self.request.user}')
            logger.info(f'[place/{place.id}/] add contributor: {self.request.user}')
            anime.save()
            place.save()

    def perform_create(self, serializer):
        self.update_contributor()
        serializer.save()

    def perform_update(self, serializer):
        self.update_contributor()
        serializer.save()
