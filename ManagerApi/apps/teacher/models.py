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
