from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from users.models import User, UserAnimeCollection
from .filters import AnimeFilter
from .models import Anime
from .serializers import AnimeDetailSerializer


class AnimeViewSet(ModelViewSet):
    """
    Anime ViewSet
    """
    queryset = Anime.objects.all()
    serializer_class = AnimeDetailSerializer
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

    @action(methods=['post', 'delete'], detail=True)
    def collection(self, request, pk=None):
        """
        anime 收藏
        """
        anime = self.get_object()
        # user = request.user
        user = User.objects.get(pk=1)
        if not user.is_authenticated:
            raise AuthenticationFailed('用户未登录', code='not_authenticated')

        if request.method == 'POST':  # 添加
            user_anime_collection = UserAnimeCollection(user=user, anime=anime)
            anime.collection_num += 1
            user_anime_collection.save()
            anime.save()
            return Response(status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':  # 删除
            user_anime_collection = UserAnimeCollection.objects.filter(user=user, anime=anime)
            anime.collection_num -= 1
            user_anime_collection.delete()
            anime.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

