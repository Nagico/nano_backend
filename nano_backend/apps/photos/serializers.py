from rest_framework.serializers import ModelSerializer, ListSerializer

import users.models
from nano_backend.utils.choices import StatusChoice
from .models import Photo


class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'
        read_only_fields = ['create_user', 'status']

    def validate(self, attrs):
        # attrs['create_user'] = self.context['request'].user
        # attrs['contributor'] = self.context['request'].user
        attrs['create_user'] = users.models.User.objects.get(pk=1)
        attrs['status'] = StatusChoice.PENDING
        return attrs


class PhotoInfoList(ListSerializer):
    def to_representation(self, data):
        data = data.filter(status=StatusChoice.PASS)
        return super(PhotoInfoList, self).to_representation(data)


class PhotoInfoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        list_serializer_class = PhotoInfoList
        fields = ['id', 'name', 'image']
