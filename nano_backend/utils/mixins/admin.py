# 各类权限
class AdminMixin:
    """
    Admin mixin 基类
    """
    pass


class StaffPermAdminMixin(AdminMixin):
    """
    员工权限检测
    """
    def check_perm_staff(self, user_obj):
        if not user_obj.is_active or user_obj.is_anonymous:
            return False
        if user_obj.is_superuser or user_obj.is_staff:
            return True
        return False


class SuperUserPermAdminMixin(AdminMixin):
    """
    超级用户权限检测
    """
    def check_perm_superuser(self, user_obj):
        if user_obj.is_active and user_obj.is_superuser:
            return True
        if not user_obj.is_active or user_obj.is_anonymous or user_obj.is_staff:
            return False
        return False


class StaffViewAdminMixin(StaffPermAdminMixin):
    """
    staff 及以上查看权限
    """
    def has_view_permission(self, request, obj=None):
        return self.check_perm_staff(request.user)


class StaffAddAdminMixin(StaffPermAdminMixin):
    """
    staff 及以上添加权限
    """
    def has_add_permission(self, request):
        return self.check_perm_staff(request.user)


class StaffChangeAdminMixin(StaffPermAdminMixin):
    """
    staff 及以上修改权限
    """
    def has_change_permission(self, request, obj=None):
        return self.check_perm_staff(request.user)


class StaffDeleteAdminMixin(StaffPermAdminMixin):
    """
    staff 及以上删除权限
    """
    def has_delete_permission(self, request, obj=None):
        return self.check_perm_staff(request.user)


class SuperUserViewAdminMixin(SuperUserPermAdminMixin):
    """
    superuser 及以上查看权限
    """
    def has_view_permission(self, request, obj=None):
        return self.check_perm_superuser(request.user)


class SuperUserAddAdminMixin(SuperUserPermAdminMixin):
    """
    superuser 及以上添加权限
    """
    def has_add_permission(self, request):
        return self.check_perm_superuser(request.user)


class SuperUserChangeAdminMixin(SuperUserPermAdminMixin):
    """
    superuser 及以上修改权限
    """
    def has_change_permission(self, request, obj=None):
        return self.check_perm_superuser(request.user)


class SuperUserDeleteAdminMixin(SuperUserPermAdminMixin):
    """
    superuser 及以上删除权限
    """
    def has_delete_permission(self, request, obj=None):
        return self.check_perm_superuser(request.user)


class StaffRequiredAdminMixin(StaffViewAdminMixin,
                              StaffAddAdminMixin,
                              StaffChangeAdminMixin,
                              StaffDeleteAdminMixin):
    """
    只有管理员才能访问
    """
    pass


class SuperuserRequiredAdminMixin(SuperUserViewAdminMixin,
                                  SuperUserAddAdminMixin,
                                  SuperUserChangeAdminMixin,
                                  SuperUserDeleteAdminMixin):
    """
    只有超级管理员才能访问
    """
    pass


class StaffReadOnlyAdminMixin(StaffViewAdminMixin,
                              SuperUserAddAdminMixin,
                              SuperUserChangeAdminMixin,
                              SuperUserDeleteAdminMixin):
    """
    只有管理员才能访问
    """
    pass
