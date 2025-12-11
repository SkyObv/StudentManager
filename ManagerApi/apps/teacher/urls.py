from django.urls import path,include
from .views import GetStudentListView, ImportStudentsView, GetTaskResultView

urlpatterns = [
    path('get/allStudents/', GetStudentListView.as_view()),                               # 获取所有学生
    path('import/students/', ImportStudentsView.as_view()),                               # 导入学生
    path('get/status/<str:task_id>/', GetTaskResultView.as_view())                                      # 查询状态
    # 导入学生
]