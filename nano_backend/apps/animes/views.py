from rest_framework.viewsets import ModelViewSet

from nano_backend.utils.choices import StatusChoice
from .models import Anime
from .serializers import AnimeSerializer


class AnimeViewSet(ModelViewSet):
    """
    Anime ViewSet
    """
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer

    def get_queryset(self):
        return self.queryset.filter(status=StatusChoice.PASS)

    def update(self, request, *args, **kwargs):
        """
        支持部分更新
        """
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

