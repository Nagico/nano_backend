from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from animes.models import Anime
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

    def update_contributor(self):
        """
        更新贡献者
        :return:
        """
        anime = None
        if self.action == 'create':  # 创建
            if self.request.data.get('is_public', False) is True:  # 已公开
                # 从请求中获取id
                anime = Anime.objects.get(pk=self.request.data['anime_id'])
        elif self.action == 'update':  # 更新
            if self.request.data.get('is_public', False) is True:  # 已公开
                # 从数据库中查询
                photo = Place.objects.get(pk=self.kwargs['pk'])
                anime = photo.anime_id
        if anime:  # 更新贡献者
            anime.contributor.add(User.objects.get(pk=2))
            anime.save()

    def perform_create(self, serializer):
        self.update_contributor()
        serializer.save()

    def perform_update(self, serializer):
        self.update_contributor()
        serializer.save()
