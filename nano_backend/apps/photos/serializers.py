from rest_framework.serializers import ModelSerializer, ListSerializer

import users.models
from nano_backend.utils.choices import StatusChoice
from .models import Photo


class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'
        read_only_fields = ['create_user', 'is_approved']

    def validate(self, attrs):
        # attrs['create_user'] = self.context['request'].user
        attrs['create_user'] = users.models.User.objects.get(pk=1)
        return attrs
