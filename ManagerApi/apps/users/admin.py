from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, Teacher

# Register your models here.
@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['id','username','password','is_active','name']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        # 在“个人信息”分组里，加上 'name' 字段
        ('个人信息', {'fields': ('name', 'email')}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            # 在 'fields' 元组里，加上 'name'
            'fields': ('username', 'name', 'password1', 'password2'),
        }),
    )

@admin.register(Student)
class StudentAdmin(UserAdmin):
    list_display = ['id','username','password','is_active','name']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        # 在“个人信息”分组里，加上 'name' 字段
        ('个人信息', {'fields': ('name', 'email')}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            # 在 'fields' 元组里，加上 'name'
            'fields': ('username', 'name', 'password1', 'password2'),
        }),
    )

@admin.register(Teacher)
class TeacherAdmin(UserAdmin):
    list_display = ['id','username','password','is_active','name']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        # 在“个人信息”分组里，加上 'name' 字段
        ('个人信息', {'fields': ('name', 'email')}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            # 在 'fields' 元组里，加上 'name'
            'fields': ('username', 'name', 'password1', 'password2'),
        }),
    )