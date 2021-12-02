from rest_framework.viewsets import ModelViewSet
from django.db.models import Q

from users.models import User
from .models import Anime
from .serializers import AnimeSerializer


class AnimeViewSet(ModelViewSet):
    """
    Anime ViewSet
    """
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer

    def get_queryset(self):
        return self.queryset.filter(Q(is_approved=True) | Q(create_user=User.objects.get(pk=1)))

    def update(self, request, *args, **kwargs):
        """
        支持部分更新
        """
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

