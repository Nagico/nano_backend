from django.db.models import Q
from rest_framework.serializers import ListSerializer

from users.models import User


class LimitedListSerializer(ListSerializer):
    """
    用于外键序列化过滤
    """
    def filter_data(self, data):
        return data.filter(Q(is_approved=True) | Q(create_user=self.context['request'].user.id))[:20]

    def to_representation(self, data):
        data = self.filter_data(data)
        return super(LimitedListSerializer, self).to_representation(data)
