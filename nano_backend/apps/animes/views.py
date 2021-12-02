from django.core.files.uploadhandler import MemoryFileUploadHandler
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Anime
from .serializers import AnimeSerializer


class AnimeViewSet(ModelViewSet):
    """
    Anime ViewSet
    """
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
