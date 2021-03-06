import logging

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from nano_backend.utils.auth import check_permission
from nano_backend.utils.mixins.views import CacheListModelMixin, CacheRetrieveModelMixin
from users.models import UserAnimeCollection, UserAnimeHistory
from .filters import AnimeFilter
from .models import Anime
from .serializers import AnimeDetailSerializer, AnimeInfoSerializer

logger = logging.getLogger(__name__)

CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 60 * 1)


class AnimeViewSet(CacheListModelMixin, CacheRetrieveModelMixin, ModelViewSet):
    """
    Anime ViewSet
    """
    queryset = Anime.objects.filter(is_public=True, is_approved=True)
    serializer_class = AnimeDetailSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]  # 排序 过滤

    ordering_fields = ['id', 'create_time', 'update_time', 'title', 'title_cn', 'is_approved', 'is_public',
                       'create_user', 'collection_num']  # 排序字段
    filterset_class = AnimeFilter  # 自定义过滤器

    permission_classes = [AllowAny]  # 允许任何人

    def get_serializer(self, *args, **kwargs):
        """
        动态获取序列化器
        """
        kwargs.setdefault('context', self.get_serializer_context())
        if self.action == 'list':
            return AnimeInfoSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        """
        重写list 添加搜索选项
        """
        search_key = request.query_params.get('search', '')
        if search_key:
            queryset = self.filter_queryset(self.get_queryset().filter(
                Q(title__icontains=search_key) | Q(title_cn__icontains=search_key) | Q(alias__title__icontains=search_key)
            ).distinct())
        else:
            queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        创建动画
        """

        check_permission(self)

        logger.info(f'[anime/] user {request.user} create anime: {request.data}')
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        更新动画
        """

        check_permission(self)

        kwargs['partial'] = True
        logger.info(f'[anime/{kwargs["pk"]}/] user {request.user} update anime: {request.data}')
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        """
        更新时删除图片
        """
        instance = self.get_object()
        if 'cover' in serializer.validated_data:
            instance.cover.delete()
        if 'cover_small' in serializer.validated_data:
            instance.cover_small.delete()
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """
        删除动画
        """

        check_permission(self)

        logger.info(f'[anime/{kwargs["pk"]}/] user {request.user} delete anime')
        return super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        """
        添加删除图片
        """
        instance.cover.delete()
        instance.cover_small.delete()
        instance.delete()

    @action(methods=['get', 'post', 'delete'], detail=True)
    def collection(self, request, pk=None):
        """
        anime 收藏增删
        """
        anime = self.get_object()  # 传入pk的对应anime
        user = request.user  # 获取当前登录用户
        if not user.is_authenticated:  # 当前用户未登录
            raise AuthenticationFailed('用户未登录', code='not_authenticated')

        # 添加
        if request.method == 'POST':
            if UserAnimeCollection.objects.filter(user=user, anime=anime).exists():
                raise PermissionDenied('已收藏', code='already_collected')

            user_anime_collection = UserAnimeCollection(user=user, anime=anime)  # 联合表添加
            anime.collection_num += 1
            user_anime_collection.save()
            anime.save()
            logger.info(f'[anime/{pk}/] user {user} add anime to collection')
            return Response({'is_collected': True}, status=status.HTTP_201_CREATED)
        # 删除
        elif request.method == 'DELETE':
            if not UserAnimeCollection.objects.filter(user=user, anime=anime).exists():
                raise PermissionDenied('未收藏', code='not_collected')

            user_anime_collection = UserAnimeCollection.objects.get(user=user, anime=anime)  # 联合表删除
            anime.collection_num -= 1
            user_anime_collection.delete()
            anime.save()
            logger.info(f'[anime/{pk}/] user {user} delete anime from collection')
            return Response(status=status.HTTP_204_NO_CONTENT)
        # 查询
        elif request.method == 'GET':
            is_collected = UserAnimeCollection.objects.filter(user=user, anime=anime).exists()
            return Response({'is_collected': is_collected}, status=status.HTTP_200_OK)

    @action(methods=['get', 'post', 'delete'], detail=True)
    def history(self, request, pk=None):
        """
        anime 历史增删
        """
        anime = self.get_object()  # 传入pk的对应anime
        user = request.user  # 获取当前登录用户
        if not user.is_authenticated:  # 当前用户未登录
            raise AuthenticationFailed('用户未登录', code='not_authenticated')

        # 添加
        if request.method == 'POST':
            if UserAnimeHistory.objects.filter(user=user, anime=anime).exists():
                UserAnimeHistory.objects.get(user=user, anime=anime).delete()

            user_anime_history = UserAnimeHistory(user=user, anime=anime)  # 联合表添加
            user_anime_history.save()
            logger.info(f'[anime/{pk}/] user {user} add history')
            return Response(status=status.HTTP_201_CREATED)
        # 删除
        elif request.method == 'DELETE':
            if not UserAnimeHistory.objects.filter(user=user, anime=anime).exists():
                raise PermissionDenied('无历史', code='not_history')

            user_anime_history = UserAnimeHistory.objects.get(user=user, anime=anime)  # 联合表删除
            user_anime_history.delete()
            logger.info(f'[anime/{pk}/] user {user} delete anime from history')
            return Response(status=status.HTTP_204_NO_CONTENT)
        # 查询
        elif request.method == 'GET':
            return Response({}, status=status.HTTP_200_OK)
