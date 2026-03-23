from django.db import models

# 宿舍申请记录模型
class HostelApply(models.Model):
    teacher = models.ForeignKey(
        'users.User',
        verbose_name='申请老师',
        on_delete=models.CASCADE,                                    # 级联删除
        related_name='teacher_apply',                                # 反向查询
        limit_choices_to={'user_type': 'teacher'}
    )
    hostel = models.ForeignKey(
        'users.Hostel',
        verbose_name='申请宿舍',
        on_delete=models.CASCADE,                                    # 级联删除
        related_name='hostel_apply',                                 # 反向查询
    )
    apply_time = models.DateTimeField(
        verbose_name='申请时间',
        auto_now_add=True
    )
    apply_state = models.CharField(
        verbose_name='申请状态',
        max_length=20,
        choices=(('待审核','待审核'),('通过','通过'),('拒绝','拒绝')),
        default='待审核',
    )
    class Meta:
        verbose_name = '宿舍申请记录'
        verbose_name_plural = verbose_name
        ordering = ['-apply_time']
        unique_together = ('teacher','hostel')

# 门禁卡模型
class TripsLog(models.Model):
    number = models.CharField(max_length=100,verbose_name='卡号',db_index=True,unique=True)
    manager_teacher = models.ForeignKey(
        'users.User',
        related_name='trips',
        null=True,                                     # 允许数据库为空
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={'user_type': 'teacher'},     # 限制可选项为教师类型
        verbose_name='门禁卡管理者老师'
    )
    student = models.OneToOneField(
        'users.User',
        related_name='key',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={'user_type': 'student'},
        verbose_name='关联学生'
    )
    in_hostel = models.BooleanField(default=False,verbose_name='是否在宿舍')
    update_time = models.DateTimeField(auto_now=True,verbose_name='刷卡时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    key_card_state = models.BooleanField(verbose_name='门禁卡状态', default=True)
    class Meta:
        verbose_name = '门禁卡'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.number
