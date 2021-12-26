# 权限控制
from rest_framework.exceptions import PermissionDenied as DRFPermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication as DRFJWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken

from nano_backend.utils.exceptions import EmptyPermissionDenied


def check_permission(view):
    """
    检查权限

    :param view: 传入的视图
    """
    if not view.request.user.is_authenticated:
        raise AuthenticationFailed('用户未登录', code='not_authenticated')
    if hasattr(view.kwargs, 'pk'):  # 详情视图
        if view.request.user != view.get_object().create_user:
            raise DRFPermissionDenied('该用户没有权限', code='permission_denied')


class JWTAuthentication(DRFJWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)

        except InvalidToken:
            raise EmptyPermissionDenied()

        return self.get_user(validated_token), validated_token
