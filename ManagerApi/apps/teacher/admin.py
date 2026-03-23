from django.contrib import admin
from .models import HostelApply, TripsLog

# 宿舍楼模型后台管理
@admin.register(HostelApply)
class HostelApplyAdmin(admin.ModelAdmin):
    list_display = ('id','teacher', 'hostel','apply_time','apply_state',)                # 列表页显示的字段
    list_filter = ('apply_state',)                                                       # 右侧过滤器

# 门禁卡id
@admin.register(TripsLog)
class TripsLogAdmin(admin.ModelAdmin):
    list_display = ['id','number','student','in_hostel','update_time','create_time','key_card_state']
    list_filter = ['key_card_state']