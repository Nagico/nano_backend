from django.contrib import admin

from .models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_per_page = 20  # 每页显示条数
    list_display = ['id', 'name', 'address', 'anime_id', 'is_public', 'is_approved',
                    'create_user', 'update_time', 'create_time']
    list_display_links = ['id', 'name']
    list_filter = ['is_public', 'is_approved', 'create_user', 'update_time', 'create_time']
    search_fields = ['name', 'address', 'anime_id__title_cn', 'anime_id__title', 'create_user__username']
