from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from users.models import UserAnimeCollection
from .filters import AnimeFilter
from .models import Anime
from .serializers import AnimeDetailSerializer


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
            return Anime.objects.filter(is_public=True)

    def update(self, request, *args, **kwargs):
        """
        支持部分更新
        """
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    @action(methods=['post', 'delete'], detail=True)
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
            user_anime_collection = UserAnimeCollection(user=user, anime=anime)  # 联合表添加
            anime.collection_num += 1
            user_anime_collection.save()
            anime.save()
            return Response(status=status.HTTP_201_CREATED)
        # 删除
        elif request.method == 'DELETE':
            user_anime_collection = UserAnimeCollection.objects.filter(user=user, anime=anime)  # 联合表删除
            anime.collection_num -= 1
            user_anime_collection.delete()
            anime.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

