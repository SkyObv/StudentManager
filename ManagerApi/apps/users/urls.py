from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView, StudentListView,FloorListView,HostelListView,CreateFloorView,FloorDeleteView, CreateHostelView,HostelDeleteView, DeleteStudentFromHostelView, AssignStudentToHostelView

urlpatterns = [
    path('login/',CustomTokenObtainPairView.as_view()),              # 登入
    path('refresh/',TokenRefreshView.as_view()),                     # 刷新

    path('floors/',FloorListView.as_view()),                         # 获取所有楼层
    path('hostel/<int:floor_id>/',HostelListView.as_view()),         # 获取单个楼层的所有宿舍信息
    path('students/',StudentListView.as_view()),                     # 获取所有学生

    path('create/floor/',CreateFloorView.as_view()),                 # 创建楼层
    path('delete/<int:pk>/floor',FloorDeleteView.as_view()),         # 删除楼层

    path('create/hostel/',CreateHostelView.as_view()),               # 创建宿舍
    path('delete/<int:pk>/hostel/',HostelDeleteView.as_view()),      # 删除宿舍

    path('delete/fromhostel/student/',DeleteStudentFromHostelView.as_view()), # 从宿舍中删除学生
    path('add/fromhostel/student/',AssignStudentToHostelView.as_view()), # 为学生分配宿舍
]