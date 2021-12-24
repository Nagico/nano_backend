from django.contrib import admin

from nano_backend.utils.mixins.admin import StaffRequiredAdminMixin
from .models import Place


@admin.register(Place)
class PlaceAdmin(StaffRequiredAdminMixin, admin.ModelAdmin):
    list_per_page = 20  # 每页显示条数
    list_display = ['id', 'name', 'city', 'address', 'anime_id', 'is_public', 'is_approved',
                    'create_user', 'update_time', 'create_time']
    list_display_links = ['id', 'name']
    list_filter = ['is_public', 'city', 'is_approved', 'create_user', 'update_time', 'create_time']
    search_fields = ['id', 'name', 'city', 'address', 'anime_id__title_cn', 'anime_id__title', 'create_user__username']
    autocomplete_fields = ['anime']  # 带有搜索框的外键选择框
