import logging

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
from users.models import UserAnimeCollection
from .filters import AnimeFilter
from .models import Anime
from .serializers import AnimeDetailSerializer, AnimeInfoSerializer

logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(
        description='分页获取动画列表',
        tags=['Anime'],
        responses={
            status.HTTP_200_OK: AnimeDetailSerializer(many=True),
        },
    ),
)
class AnimeViewSet(ModelViewSet):
    """
    Anime ViewSet
    """
    serializer_class = AnimeDetailSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]  # 排序 过滤

    ordering_fields = ['id', 'create_time', 'update_time', 'title', 'title_cn', 'is_approved', 'is_public',
                       'create_user', 'anime_id']  # 排序字段
    filterset_class = AnimeFilter  # 自定义过滤器

    permission_classes = [AllowAny]  # 允许任何人

    def get_queryset(self):
        """
        动态获取查询集，根据登录情况返回
        :return:
        """
        user = self.request.user  # 获取当前用户

        if user.is_authenticated:  # 用户已登录
            return Anime.objects.filter(Q(create_user=user) | Q(is_public=True))
        else:  # 用户未登录
            return Anime.objects.filter(is_public=True, is_approved=True)

    def get_serializer(self, *args, **kwargs):
        """
        动态获取序列化器
        """
        kwargs.setdefault('context', self.get_serializer_context())
        if self.action == 'list':
            return AnimeInfoSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

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
