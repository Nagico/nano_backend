import logging

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from animes.models import Anime
from users.models import User, UserPlaceCollection
from .filters import PlaceFilter
from .models import Place
from .serializers import PlaceDetailsSerializer

logger = logging.getLogger(__name__)


class PlaceViewSet(ModelViewSet):
    serializer_class = PlaceDetailsSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]  # 排序 过滤

    ordering_fields = ['id', 'create_time', 'update_time', 'name', 'is_approved', 'is_public', 'create_user', 'anime_id']  # 排序字段
    filterset_class = PlaceFilter  # 自定义过滤器

    permission_classes = [AllowAny]  # 允许任何人

    def update(self, request, *args, **kwargs):
        """
        支持部分更新
        """
        if not request.user.is_authenticated:
            raise AuthenticationFailed('用户未登录', code='not_authenticated')
        if request.user != Place.objects.get(pk=kwargs['pk']).create_user:
            raise PermissionDenied('该用户没有权限', code='permission_denied')

        kwargs['partial'] = True
        logger.info(f'[place/] user {request.user} update place: {request.data}')
        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise AuthenticationFailed('用户未登录', code='not_authenticated')

        logger.info(f'[place/{kwargs["pk"]}/] user {request.user} create place: {request.data}')
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise AuthenticationFailed('用户未登录', code='not_authenticated')
        if request.user != Anime.objects.get(pk=kwargs['pk']).create_user:
            raise PermissionDenied('该用户没有权限', code='permission_denied')

        logger.info(f'[anime/{kwargs["pk"]}/] user {request.user} delete place')
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        """
        动态获取查询集，根据登录情况返回
        :return:
        """
        user = self.request.user  # 获取当前用户

        if user.is_authenticated:  # 用户已登录
            return Place.objects.filter(Q(create_user=user) | Q(is_public=True))
        else:  # 用户未登录
            return Place.objects.filter(is_public=True)

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
            anime.contributor.add(self.request.user)
            logger.info(f'[anime/{anime.id}/] add contributor: {self.request.user}')
            anime.save()

    def perform_create(self, serializer):
        self.update_contributor()
        serializer.save()

    def perform_update(self, serializer):
        self.update_contributor()
        serializer.save()

    @action(methods=['post', 'delete'], detail=True)
    def collection(self, request, pk=None):
        """
        place 收藏增删
        """
        place = self.get_object()
        user = request.user  # 获取当前用户
        if not user.is_authenticated:
            raise AuthenticationFailed('用户未登录', code='not_authenticated')

        if request.method == 'POST':  # 添加
            user_place_collection = UserPlaceCollection(user=user, place=place)
            place.collection_count += 1
            user_place_collection.save()
            place.save()
            logger.info(f'[place/{pk}/collection] add collection: {request.user}')
            return Response(status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':  # 删除
            user_place_collection = UserPlaceCollection.objects.get(user=user, place=place)
            place.collection_num -= 1
            user_place_collection.delete()
            place.save()
            logger.info(f'[place/{pk}/collection] delete collection: {request.user}')
            return Response(status=status.HTTP_204_NO_CONTENT)
