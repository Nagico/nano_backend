from rest_framework.serializers import ModelSerializer, ListSerializer

import users.models
from nano_backend.utils.choices import StatusChoice
from photos.serializers import PhotoInfoSerializer
from .models import Place


class PlaceSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'
        read_only_fields = ['photo', 'create_user', 'contributor', 'status']

    def validate(self, attrs):
        # attrs['create_user'] = self.context['request'].user
        # attrs['contributor'] = self.context['request'].user
        attrs['create_user'] = users.models.User.objects.get(pk=1)
        attrs['contributor'] = [users.models.User.objects.get(pk=1)]
        attrs['status'] = StatusChoice.PENDING
        return attrs


class PlaceInfoList(ListSerializer):
    def to_representation(self, data):
        data = data.filter(status=StatusChoice.PASS)
        return super(PlaceInfoList, self).to_representation(data)


class PlaceInfoSerializer(ModelSerializer):
    class Meta:
        model = Place
        list_serializer_class = PlaceInfoList
        fields = ['id', 'name']


class PlacePhotoSerializer(ModelSerializer):
    photo = PhotoInfoSerializer(read_only=True, many=True)

    class Meta:
        model = Place
        fields = ['photo']
