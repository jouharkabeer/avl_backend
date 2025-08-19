from django.contrib import admin
from .models import Permission, Role, UserType, User

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('permission_name', 'status', 'created_at')
    search_fields = ('permission_name',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'status', 'created_at')
    search_fields = ('role_name',)

@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('user_type_name', 'status')
    search_fields = ('user_type_name',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'is_active', 'created_at')
    search_fields = ('username', 'email')
