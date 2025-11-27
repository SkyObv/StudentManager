from django.db import models
from django.contrib.auth.models import AbstractUser

# 用户模型
class User(AbstractUser):
    """用户模型"""
    USER_TYPE = (
        ('student','学生'),
        ('teacher','教师'),
        ('admin','管理员'),
    )
    # 用户类型
    user_type = models.CharField(max_length=10,verbose_name='用户类型',choices=USER_TYPE,default='student')
    # 学生关联老师字段
    teacher_id = models.ForeignKey(
        'self',
        verbose_name='指导教师',
        null=True,                                                   # 数据库允许为NULL
        blank=True,                                                  # 允许为空
        on_delete=models.SET_NULL,                                   # 指定删除时，关联对象设置为NULL
        related_name='students',                                     # 反向查询
        limit_choices_to={'user_type': 'teacher'}                    # 限制可选项为教师类型
    )
    # 学生用户关联宿舍门号
    house_number = models.ForeignKey(
        'Hostel',
        verbose_name='宿舍门牌号',
        null=True,                                                   # 允许为NULL
        blank=True,                                                  # 允许为空
        on_delete=models.SET_NULL,                                   # 删除时设置为NULL
        related_name='students_house',                               # 反向查询
    )
    # 用户性别
    gender = models.CharField(max_length=10,verbose_name='性别',choices=(('male','男'),('female','女')),default='male')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.last_name + self.first_name

# 宿舍模型
class Hostel(models.Model):
    """宿舍模型"""
    hostel_number = models.CharField(max_length=30,verbose_name='宿舍门牌号')
    floor = models.ForeignKey(
        'Floor',
        verbose_name='宿舍楼',
        on_delete=models.CASCADE,                                    # 级联删除
        related_name='hostels',                                      # 反向查询楼层
    )
    # 宿舍床位数
    capacity = models.PositiveIntegerField(
        verbose_name='床位数',
        default=6
    )
    # 用户性别
    gender = models.CharField(max_length=10, verbose_name='性别', choices=(('male', '男'), ('female', '女')),default='male')
    is_deleted = models.BooleanField(default=False,verbose_name='是否删除')
    class Meta:
        verbose_name = '宿舍'
        verbose_name_plural = verbose_name
        # 联合唯一约束：在同一个宿舍楼内，门牌号不能重复
        unique_together = ('floor', 'hostel_number')
    def __str__(self):
        return f"{self.floor.floor_name}-{self.hostel_number}"
    # 宿舍床位数动态计算,虚拟字段
    @property
    def student_count(self):
        # students_house' 是我们在 User 模型中定义的 related_name
        return self.students_house.count()
    # 宿舍床铺是否已满
    @property
    def is_full(self):
        return self.student_count >= self.capacity
    # 是否有人
    @property
    def have_people(self):
        return self.student_count > 0

# 楼层模型
class Floor(models.Model):
    """宿舍楼模型"""
    floor_name = models.CharField(max_length=20,verbose_name='宿舍楼名称',unique=True)
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')
    class Meta:
        verbose_name = '宿舍楼'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.floor_name