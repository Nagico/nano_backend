from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views


urlpatterns = [
    path('info/', views.UserInfoViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy"
    })),  # 用户信息
    path('login/', views.LoginTokenObtainPairView.as_view(), name='token_obtain_pair'),  # 登录
    path('register/', views.RegisterView.as_view(), name='token_obtain_pair'),  # 注册
    re_path(r'users/(?P<username>\w{5,20})/count/', views.UsernameCountView.as_view()),  # 用户名数量
    re_path(r'mobiles/(?P<mobile>1[3-9]\d{9})/count/', views.MobileCountView.as_view()),  # 手机号数量
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新token
]
