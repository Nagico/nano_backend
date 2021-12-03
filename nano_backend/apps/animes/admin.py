from django.contrib import admin

from .models import Anime


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_per_page = 20  # 每页显示条数
    list_display = ['id', 'title', 'title_cn', 'is_public', 'is_approved', 'update_time', 'create_time']  # 列表显示字段
    list_display_links = ['id', 'title', 'title_cn']  # 列表可点击字段
    list_filter = ['is_public', 'is_approved', 'update_time', 'create_time']  # 过滤器
    search_fields = ['title', 'title_cn']  # 搜索字段

