from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework import routers
from django.views.static import serve
from django.conf import settings
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from users import views as user_views


urlpatterns = [
    path('admin/', admin.site.urls),  # admin 后台管理
    path('user/', include('users.urls')),  # 用户相关
    path('', include('verifications.urls')),  # 验证模块
    path('anime/', include('animes.urls')),  # 番剧
    path('place/', include('places.urls')),  # 地点
    path('photo/', include('photos.urls')),  # 照片

    url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),  # 媒体文件

    path('api_schema/', SpectacularAPIView.as_view(), name='schema'),  # API 文档
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # swagger接口文档

]

router = routers.DefaultRouter()

urlpatterns += router.urls
