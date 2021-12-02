import django_filters
from django_filters.rest_framework import FilterSet

from animes.models import Anime


class AnimeFilter(FilterSet):
    """
    anime 过滤器
    """

    id = django_filters.NumberFilter(field_name='id', lookup_expr='exact')  # ID
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')  # 标题
    title_cn = django_filters.CharFilter(field_name='title_cn', lookup_expr='icontains')  # 中文标题
    create_user = django_filters.NumberFilter(field_name='create_user', lookup_expr='exact')  # 创建用户
    is_public = django_filters.BooleanFilter(field_name='is_public', lookup_expr='exact')  # 是否公开
    is_approved = django_filters.BooleanFilter(field_name='is_approved', lookup_expr='exact')  # 是否审核通过

    class Meta:
        # 指定模型
        models = Anime
        # 指定查询的字段
        fields = ['id', 'title', 'title_cn', 'create_user', 'is_public', 'is_approved']
