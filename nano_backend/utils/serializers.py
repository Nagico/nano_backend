from django.db.models import Q
from rest_framework.serializers import ListSerializer

from users.models import User


class LimitedListSerializer(ListSerializer):
    """
    用于外键序列化过滤
    """
    def to_representation(self, data):
        data = data.filter(Q(is_approved=True) | Q(create_user=User.objects.get(pk=1)))[:20]
        return super(LimitedListSerializer, self).to_representation(data)
