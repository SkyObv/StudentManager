from django.urls import path,include
from .views import (GetStudentListView, ImportStudentsView, GetTaskResultView, GetDormitoryListView,
                    ApplyHostelView, GetApplyRecordView, ApplyRecordView, DeleteApplyRecordView
                    ,GetAllMyHostelView)

urlpatterns = [
    path('get/allStudents/', GetStudentListView.as_view()),                               # 获取所有学生
    path('import/students/', ImportStudentsView.as_view()),                               # 导入学生
    path('get/status/<str:task_id>/', GetTaskResultView.as_view()),                       # 查询状态

    # 宿舍申请
    path('get/hostel/', GetDormitoryListView.as_view()),                                  # 获取可申请的宿舍列表
    path('apply/hostel/', ApplyHostelView.as_view()),                                     # 申请宿舍

    # 申请记录
    path('get/applyRecord/', GetApplyRecordView.as_view()),                               # 获取申请记录
    path('apply/upadte/<int:pk>/', ApplyRecordView.as_view()),                            # 记录更新
    path('apply/delete/<int:pk>/',DeleteApplyRecordView.as_view()),                       # 删除记录

    # 我的宿舍
    path('myhostel/allget/',GetAllMyHostelView.as_view()),                                # 获取我的宿舍所有信息(学生)
]