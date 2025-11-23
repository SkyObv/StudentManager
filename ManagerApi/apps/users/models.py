from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Create your models here.
# 用户模型类('admins','teacher','student')
class User(AbstractUser):
    """用户模型类"""
    name = models.CharField(max_length=100, unique=False, default='待设置姓名', verbose_name='姓名')

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="admin_users",  # 唯一的反向关系名
        related_query_name="admin_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="admin_users",  # 唯一的反向关系名
        related_query_name="admin_user",
    )

    class Meta:
        db_table = 'users'
        verbose_name = '管理员用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 学生模型
class Student(AbstractUser):
    """学生模型类"""
    name = models.CharField(max_length=100, unique=False, default='待设置姓名', verbose_name='姓名')
    gender = models.CharField(max_length=10, choices=(('男', '男'), ('女', '女'), ('未知', '未知')), default='未知', verbose_name='性别')
    class_ban = models.ForeignKey('ClassBan', verbose_name='班级', on_delete=models.CASCADE, null=True,blank=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="student_users", # 唯一的反向关系名
        related_query_name="student_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="student_users", # 唯一的反向关系名
        related_query_name="student_user",
    )

    class Meta:
        db_table = 'students'
        verbose_name = '学生用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Teacher(AbstractUser):
    """教师模型类"""
    name = models.CharField(max_length=100, unique=False, default='待设置姓名', verbose_name='姓名')

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="teacher_users", # 唯一的反向关系名
        related_query_name="teacher_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="teacher_users", # 唯一的反向关系名
        related_query_name="teacher_user",
    )

    class Meta:
        db_table = 'teachers'
        verbose_name = '教师用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 班级模型
class ClassBan(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='班级序号')
    grade = models.CharField(max_length=10,
                             choices=(('初一', '初一'), ('初二', '初二'), ('初三', '初三'), ('未知', '未知')),
                             default='未知', verbose_name='所属年级')
    teacher = models.ForeignKey('Teacher', verbose_name='任课老师', on_delete=models.CASCADE)
    class Meta:
        db_table = 'class_bans'
        verbose_name = '班级'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name