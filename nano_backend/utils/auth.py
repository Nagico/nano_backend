# 权限控制
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.exceptions import AuthenticationFailed


def check_permission(view):
    """
    检查权限

    :param view: 传入的视图
    """
    if not view.request.user.is_authenticated:
        raise AuthenticationFailed('用户未登录', code='not_authenticated')
    if not view.action == 'GET':
        if view.request.user != view.get_object().create_user:
            raise PermissionDenied('该用户没有权限', code='permission_denied')
