from django.contrib import admin

from nano_backend.utils.mixins.admin import StaffRequiredAdminMixin
from .models import Anime, AnimeAlias


class AnimeAliasInline(admin.TabularInline):
    # 商品详情内联
    extra = 1    # 默认打开创建数量
    model = AnimeAlias


@admin.register(Anime)
class AnimeAdmin(StaffRequiredAdminMixin, admin.ModelAdmin):
    list_per_page = 20  # 每页显示条数
    list_display = ['id', 'title', 'title_cn', 'is_public', 'is_approved', 'update_time', 'create_time']  # 列表显示字段
    list_display_links = ['id', 'title', 'title_cn']  # 列表可点击字段
    list_filter = ['is_public', 'is_approved', 'update_time', 'create_time']  # 过滤器
    search_fields = ['id', 'title', 'title_cn']  # 搜索字段
    inlines = [AnimeAliasInline]

