from rest_framework.viewsets import ModelViewSet

from .models import Place
from .serializers import PlaceSerializer


class PlaceViewSet(ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    