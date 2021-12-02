import logging
from django.conf import settings
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, UserAnimeCollection, UserPlaceCollection
from .serializers import UserSerializer, LoginTokenObtainPairSerializer, CreateUserSerializer, UserInfoSerializer, \
    UserAnimeCollectionSerializer, UserPlaceCollectionSerializer

logger = logging.getLogger(__name__)


class UserDetailViewSet(RetrieveModelMixin,
                        UpdateModelMixin,
                        DestroyModelMixin,
                        GenericViewSet):
    """
    该用户信息视图
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # authentication_classes = [UserActiveAuthentication]  # 不检测是否激活
    # permission_classes = [IsAuthenticated]  # 仅登录用户可访问个人信息
    permission_classes = [AllowAny]  # 测试使用

    def validate_avatar(self, value):
        """
        头像检测
        """
        if not value:  # 未找到头像文件
            return settings.DEFAULT_AVATAR_PATH

        if value.content_type not in ['image/jpeg', 'image/png', 'image/gif']:  # 文件类型不正确
            raise serializers.ValidationError(detail='Avatar is not a image', code='avatar_not_image')

        if value.size > 1024 * 1024 * 2:  # 头像文件大于2M
            raise serializers.ValidationError(detail='Avatar is larger than 2MB', code='avatar_too_large')
        if value.size < 1024:  # 头像文件小于1KB
            raise serializers.ValidationError(detail='Avatar is smaller than 1KB', code='avatar_too_small')

        if self.instance.avatar != settings.DEFAULT_AVATAR_PATH:  # 已存在头像文件
            self.instance.avatar.delete()  # 删除原头像文件

        return value

    def get_object(self):
        """
        重写对象获取逻辑，获取当前登录用户的信息
        """
        # obj = self.get_queryset().get(id=self.request.user.id)  # 从jwt鉴权中获取当前登录用户的uid
        obj = self.get_queryset().get(id=1)  # 从jwt鉴权中获取当前登录用户的uid
        if obj is None:
            raise NotFound('User not found', code='user_not_found')

        return obj

    def update(self, request, *args, **kwargs):
        """
        支持部分更新
        """
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class UserAnimeCollectionViewSet(GenericViewSet):
    """
    用户动画收藏视图
    """
    queryset = UserAnimeCollection.objects.all()
    serializer_class = UserAnimeCollectionSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        # queryset = self.get_queryset().filter(user=request.user)
        queryset = self.get_queryset().filter(user=User.objects.get(id=1))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserPlaceCollectionViewSet(GenericViewSet):
    """
    用户地点收藏视图
    """
    queryset = UserPlaceCollection.objects.all()
    serializer_class = UserPlaceCollectionSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        # queryset = self.get_queryset().filter(user=request.user)
        queryset = self.get_queryset().filter(user=User.objects.get(id=1))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserInfoViewSet(RetrieveModelMixin, GenericViewSet):
    """
    获取用户可公开信息
    """
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer


class LoginTokenObtainPairView(TokenObtainPairView):
    """
    用户登录 token 获取视图
    """
    serializer_class = LoginTokenObtainPairSerializer  # 指定自定义的序列化器，校验密码


class RegisterView(CreateAPIView):
    """
    用户注册
    """
    serializer_class = CreateUserSerializer


class UsernameCountView(APIView):
    """
    判断用户名是否存在
    """

    def get(self, request, username):
        count = User.objects.filter(username=username).count()

        data = {
            'username': username,
            'count': count
        }

        return Response(data)


class MobileCountView(APIView):
    """
    判断手机号是否存在
    """

    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile': mobile,
            'count': count
        }

        return Response(data)
