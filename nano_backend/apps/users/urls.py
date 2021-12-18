from django.urls import path, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from . import views


router = routers.SimpleRouter()

urlpatterns = [
    # 登录用户个人信息
    path('', views.UserDetailViewSet.as_view({  # 本用户详细信息
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='user'),
    path('anime/', views.UserAnimeCollectionViewSet.as_view({  # 本用户anime收藏
        'get': 'list'
    }), name='user'),
    path('history/', views.UserAnimeHistoryViewSet.as_view({  # 本用户历史记录
        'get': 'list'
    }), name='user'),
    path('place/', views.UserPlaceCollectionViewSet.as_view({  # 本用户place收藏
        'get': 'list'
    }), name='user'),

    # 所有用户公开信息
    path('<int:pk>/', views.UserInfoViewSet.as_view({  # 用户公开信息
        'get': 'retrieve',
    })),

    # 登陆注册
    path('login/', views.LoginTokenObtainPairView.as_view(), name='token_obtain_pair'),  # 登录
    path('register/', views.RegisterView.as_view(), name='token_obtain_pair'),  # 注册
    re_path(r'users/(?P<username>\w{5,20})/count/', views.UsernameCountView.as_view()),  # 用户名数量
    re_path(r'mobiles/(?P<mobile>1[3-9]\d{9})/count/', views.MobileCountView.as_view()),  # 手机号数量
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新token
]

