from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
IDENTITY = (
    ('student', '学生'),
    ('teacher', '教师'),
    ('admin', '管理员'),
)

# 用户模型类('admin','teacher','student')
class User(AbstractUser):
    """用户模型类"""
    IDENTITY_STUDENT = 'student'
    IDENTITY_TEACHER = 'teacher'
    IDENTITY_ADMIN = 'admin'

    name = models.CharField(max_length=100, unique=False, default='待设置姓名', verbose_name='姓名')
    identity = models.CharField(max_length=128,choices=IDENTITY, verbose_name='身份')

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 管理员选项
class AdminOptions(models.Model):
    options = models.CharField(max_length=100, unique=True ,verbose_name='管理员选项')
    is_show = models.BooleanField(default=True, verbose_name='是否显示')

    class Meta:
        db_table = 'admin_options'
        verbose_name = '管理员选项'
        verbose_name_plural = verbose_name
