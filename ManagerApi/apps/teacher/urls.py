from django.urls import path,include
from .views import GetStudentListView

urlpatterns = [
    path('get/allStudents/', GetStudentListView.as_view()),                               # 获取所有学生
    # path('import/students/', ImportStudentsView.as_view())                                 # 导入学生
]