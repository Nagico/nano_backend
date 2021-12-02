from rest_framework.viewsets import ModelViewSet

from nano_backend.utils.choices import StatusChoice
from .models import Place
from .serializers import PlaceSerializer


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

