from django.contrib import admin

from .models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_per_page = 20  # 每页显示条数
    list_display = ['id', 'name', 'type', 'is_public', 'is_approved', 'anime_id', 'place_id',
                    'create_user', 'create_time', 'update_time']
    list_display_links = ['id', 'name']
    list_filter = ['type', 'is_public', 'is_approved', 'anime_id', 'place_id', 'create_user']
    search_fields = ['name', 'type', 'is_public', 'is_approved', 'anime_id__title',
                     'anime_id__title_cn', 'place_id__name', 'create_user__username']
