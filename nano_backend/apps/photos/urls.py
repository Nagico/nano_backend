from django.urls import path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()

urlpatterns = [

]

router.register(r'', views.PhotoViewSet, basename='photos')  # photo 视图集

urlpatterns += router.urls
