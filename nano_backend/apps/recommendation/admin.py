from django.contrib import admin

from nano_backend.utils.mixins.admin import StaffRequiredAdminMixin
from .models import Recommendation


@admin.register(Recommendation)
class RecommendationAdmin(StaffRequiredAdminMixin, admin.ModelAdmin):
    list_per_page = 20  # 每页显示条数
    list_display = ['id', 'title', 'anime', 'score', 'update_time', 'create_time']  # 列表显示字段
    list_display_links = ['id', 'title']  # 列表可点击字段
