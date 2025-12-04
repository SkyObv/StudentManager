from django.contrib import admin
from users.models import User, Hostel, Floor
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# 宿舍楼模型后台管理
@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    """
    宿舍楼模型的后台管理配置
    """
    list_display = ('id','floor_name', 'is_deleted')  # 列表页显示的字段
    list_filter = ('is_deleted',)                # 右侧过滤器
    search_fields = ('floor_name',)               # 搜索框
# 宿舍模型后台管理
@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    """
    宿舍模型的后台管理配置
    """
    list_display = ('id','hostel_number', 'floor', 'capacity', 'student_count', 'is_full', 'is_deleted')
    # list_display 中可以直接使用 @property 定义的虚拟字段
    list_filter = ('floor', 'is_deleted')        # 按宿舍楼和删除状态过滤
    search_fields = ('hostel_number', 'floor__floor_name') # 支持按门牌号和宿舍楼名搜索
    # ordering = ('floor__floor_name', 'hostel_number') # 默认排序
# 用户模型后台管理
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    用户模型的后台管理配置
    继承 Django 内置的 UserAdmin 以保留所有用户管理功能
    """
    # 在列表页显示哪些字段
    list_display = ('id','username', 'user_type', 'first_name','last_name','get_teacher', 'get_hostel', 'is_staff','is_active')
    # 在列表页添加过滤器
    list_filter = ('user_type', 'is_staff', 'is_active', 'groups')
    # 搜索框支持按哪些字段搜索
    search_fields = ('username', 'email', 'first_name', 'last_name')
    # 自定义字段集，用于组织编辑页面的布局
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('first_name', 'last_name', 'email')}),
        ('权限信息', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('重要日期', {'fields': ('last_login', 'date_joined')}),
        ('自定义信息', {'fields': ('user_type', 'teacher_id', 'house_number')}),
    )
    # 创建新用户时的字段集
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type'),
        }),
    )
    # --- 自定义方法，用于在列表页友好地显示关联对象 ---
    def get_teacher(self, obj):
        """在列表页显示指导教师的用户名"""
        if obj.teacher_id:
            return obj.teacher_id.username
        return "无"

    get_teacher.short_description = '指导教师'  # 设置列表页的表头
    def get_hostel(self, obj):
        """在列表页显示宿舍信息"""
        if obj.house_number:
            return str(obj.house_number)  # 调用 Hostel 的 __str__ 方法
        return "无"
    get_hostel.short_description = '宿舍'  # 设置列表页的表头

