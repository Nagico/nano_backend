from rest_framework import serializers

import users.models
from places.serializers import PlaceInfoSerializer
from .models import Anime


class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = '__all__'

        read_only_fields = ['place', 'create_user', 'contributor', 'status']

    def validate(self, attrs):

        # attrs['create_user'] = self.context['request'].user
        # attrs['contributor'] = self.context['request'].user
        attrs['create_user'] = users.models.User.objects.get(pk=1)
        attrs['contributor'] = [users.models.User.objects.get(pk=1)]

        return attrs


class AnimePlaceSerializer(serializers.ModelSerializer):
    place = PlaceInfoSerializer(read_only=True, many=True)

    class Meta:
        model = Anime
        fields = ['place']
