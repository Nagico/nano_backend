import django_filters
from django_filters.rest_framework import FilterSet

from places.models import Place


class PlaceFilter(FilterSet):
    """
    place 过滤器
    """

    id = django_filters.NumberFilter(field_name='id', lookup_expr='exact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    city = django_filters.CharFilter(field_name='city', lookup_expr='icontains')
    anime_id = django_filters.NumberFilter(field_name='anime_id', lookup_expr='exact')
    create_user = django_filters.NumberFilter(field_name='create_user', lookup_expr='exact')
    is_public = django_filters.BooleanFilter(field_name='is_public', lookup_expr='exact')
    is_approved = django_filters.BooleanFilter(field_name='is_approved', lookup_expr='exact')

    class Meta:
        # 指定模型
        models = Place
        # 指定查询的字段
        fields = ['id', 'name', 'address', 'anime_id', 'create_user', 'is_public', 'is_approved']
