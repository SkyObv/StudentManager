from django.contrib import admin
from .models import User, AdminOptions
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','identity']

@admin.register(AdminOptions)
class AdminOptionsAdmin(admin.ModelAdmin):
    list_display = ['id','options','is_show']
