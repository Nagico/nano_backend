from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from animes.models import Anime
from places.models import Place
from users.models import User
from .models import Photo
from .serializers import PhotoDetailSerializer


class PhotoViewSet(ModelViewSet):
    filter_backends = [OrderingFilter, DjangoFilterBackend]  # 排序 过滤
    serializer_class = PhotoDetailSerializer

    ordering_fields = ['id', 'create_time', 'update_time', 'is_approved', 'is_public', 'anime_id', 'place_id',
                       'create_user']  # 排序
    filter_fields = ['id', 'is_approved', 'is_public', 'anime_id', 'place_id', 'create_user']  # 过滤

    permission_classes = [AllowAny]  # 允许任何人

    def get_queryset(self):
        """
        动态获取查询集，根据登录情况返回
        :return:
        """
        user = self.request.user  # 获取当前用户

        if user.is_authenticated:  # 用户已登录
            return Photo.objects.filter(Q(create_user=user) | Q(is_public=True))
        else:  # 用户未登录
            return Photo.objects.filter(is_public=True)

    def update(self, request, *args, **kwargs):
        """
        支持部分更新
        """
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

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
            anime.contributor.add(User.objects.get(pk=2))
            place.contributor.add(User.objects.get(pk=2))
            anime.save()
            place.save()

    def perform_create(self, serializer):
        self.update_contributor()
        serializer.save()

    def perform_update(self, serializer):
        self.update_contributor()
        serializer.save()
