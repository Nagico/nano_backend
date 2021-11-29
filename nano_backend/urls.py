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
    path('user/', include('users.urls')),  # 用户相关
    url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
]

router = routers.DefaultRouter()

urlpatterns += router.urls
