from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from nano_backend.utils.choices import StatusChoice
from photos.models import Photo
from photos.serializers import PhotoInfoSerializer, PhotoSerializer
from .models import Place
from .serializers import PlaceSerializer, PlacePhotoSerializer


class PlaceViewSet(ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def update(self, request, *args, **kwargs):
        """
        支持部分更新
        """
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        return self.queryset.filter(status=StatusChoice.PASS)

    @action(methods=['get', 'post', 'delete'], detail=True)
    def photo(self, request, pk=None):
        """
        相关photo
        """
        place = self.get_object()
        photo_id = request.data.get('photo_id')  # 传入 pk
        if request.method == 'POST':  # 添加
            place.photo.add(photo_id)
            place.contributor.add(Photo.objects.get(pk=photo_id).create_user.id)
            return Response(self.get_photo_info(place), status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':  # 删除
            place.photo.remove(photo_id)
            return Response(self.get_photo_info(place), status=status.HTTP_200_OK)
        elif request.method == 'GET':  # 获取
            return Response(self.get_photo_info(place), status=status.HTTP_200_OK)

    def get_photo_info(self, obj):
        serializer = PlacePhotoSerializer(obj)
        return serializer.data
