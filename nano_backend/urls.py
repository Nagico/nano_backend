from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from django.views.static import serve
from django.conf import settings
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from users import views as user_views


urlpatterns = [
    path('admin/', admin.site.urls),  # admin 后台管理
    path('user/', user_views.UserInfoViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy"
    })),  # 用户信息
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 获取token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新token
    url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
]

router = routers.DefaultRouter()

urlpatterns += router.urls
