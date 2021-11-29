import logging

from django.core.files.uploadhandler import MemoryFileUploadHandler
from rest_framework.exceptions import NotFound
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import User
from .serializers import UserSerializer

logger = logging.getLogger(__name__)


class UserInfoViewSet(RetrieveModelMixin,
                      UpdateModelMixin,
                      DestroyModelMixin,
                      GenericViewSet):
    """
    用户信息视图, 该接口不属于rest风格
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # authentication_classes = [UserActiveAuthentication]  # 不检测是否激活
    # permission_classes = [IsAuthenticated]  # 仅登录用户可访问个人信息
    permission_classes = [AllowAny]  # 测试使用

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
        重写update逻辑，增加自动用户激活
        """
        request.upload_handlers = [MemoryFileUploadHandler(request)]  # 头像默认使用内存上传
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

