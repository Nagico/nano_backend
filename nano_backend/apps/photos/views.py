from rest_framework.viewsets import ModelViewSet

from .models import Photo
from .serializers import PhotoSerializer


class PhotoViewSet(ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    