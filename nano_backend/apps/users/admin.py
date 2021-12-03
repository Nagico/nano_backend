from django.contrib import admin

from .models import User
from nano_backend.utils.mixins.admin import StaffReadOnlyAdminMixin

admin.site.site_title = "Nano 后台管理系统"
admin.site.site_header = "Nano 管理"


@admin.register(User)
class UserAdmin(StaffReadOnlyAdminMixin, admin.ModelAdmin):
    list_per_page = 20  # 每页显示条数
    list_display = ['id', 'username', 'mobile', 'is_staff', 'is_active', 'is_superuser']
    list_display_links = ['id', 'username']
    search_fields = ['username', 'mobile']
    list_filter = ['is_staff', 'is_active', 'is_superuser']

