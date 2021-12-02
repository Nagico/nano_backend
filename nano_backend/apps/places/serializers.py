from rest_framework.serializers import ModelSerializer, ListSerializer

import users.models
from nano_backend.utils.choices import StatusChoice
from photos.serializers import PhotoInfoSerializer
from .models import Place


class PlaceSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'
        read_only_fields = ['photo', 'create_user', 'contributor', 'is_approved']

    def validate(self, attrs):
        # attrs['create_user'] = self.context['request'].user
        # attrs['contributor'] = self.context['request'].user
        attrs['create_user'] = users.models.User.objects.get(pk=1)
        attrs['contributor'] = [users.models.User.objects.get(pk=1)]
        return attrs
