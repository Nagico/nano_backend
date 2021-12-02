from django.core.files.uploadhandler import MemoryFileUploadHandler
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Anime
from .serializers import AnimeSerializer, AnimePlaceSerializer


class AnimeViewSet(ModelViewSet):
    """
    Anime ViewSet
    """
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer

    def update(self, request, *args, **kwargs):
        """
        支持部分更新
        """
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


    @action(methods=['get', 'post', 'delete'], detail=True)
    def place(self, request, pk=None):
        """
        相关place
        """
        anime = self.get_object()
        place_id = request.data.get('place_id')  # 传入 pk
        if request.method == 'POST':  # 添加
            anime.place.add(place_id)
            return Response(self.get_place_info(anime), status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':  # 删除
            anime.place.remove(place_id)
            return Response(self.get_place_info(anime), status=status.HTTP_200_OK)
        elif request.method == 'GET':  # 获取
            return Response(self.get_place_info(anime), status=status.HTTP_200_OK)

    def get_place_info(self, obj):
        serializer = AnimePlaceSerializer(obj)
        return serializer.data
