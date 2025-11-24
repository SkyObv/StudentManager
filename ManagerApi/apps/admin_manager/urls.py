from django.urls import path
from .views import StudentListView, StudentUpdateView, ClassBanListView

urlpatterns = [
    path('getStuidents/', StudentListView.as_view()),                # 获取所有学生
    path('getClassBans/', ClassBanListView.as_view()),               # 获取所有班级
    path('student/<int:pk>/update',StudentUpdateView.as_view())      # 修改学生信息
]