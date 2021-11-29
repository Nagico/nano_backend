from django.urls import path
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
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新token
]
