from django.urls import path, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from . import views


router = routers.SimpleRouter()

urlpatterns = [
    path('', views.UserDetailViewSet.as_view({  # 已登录详细信息
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='user'),
    path('<int:pk>/', views.UserInfoViewSet.as_view({  # 用户公开信息
        'get': 'retrieve',
    })),
    path('login/', views.LoginTokenObtainPairView.as_view(), name='token_obtain_pair'),  # 登录
    path('register/', views.RegisterView.as_view(), name='token_obtain_pair'),  # 注册
    re_path(r'users/(?P<username>\w{5,20})/count/', views.UsernameCountView.as_view()),  # 用户名数量
    re_path(r'mobiles/(?P<mobile>1[3-9]\d{9})/count/', views.MobileCountView.as_view()),  # 手机号数量
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新token
]

