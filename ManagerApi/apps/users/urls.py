from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (CustomTokenObtainPairView, StudentListView,FloorListView,HostelListView,CreateFloorView,
                    FloorDeleteView, CreateHostelView,HostelDeleteView, DeleteStudentFromHostelView,
                    AssignStudentToHostelView, TeacherListView, DeleteTeacherView, CreateUserView, RestoreTeacherView
                    , DeleteTeacherPermanentlyView, AddManagerToHostelView, GetAllHostelLogsView,GetAllCardsView,
                    CreateCardsView,UpdateCardsManagerView, DeleteCardView)

urlpatterns = [
    path('login/',CustomTokenObtainPairView.as_view()),              # 登入
    path('refresh/',TokenRefreshView.as_view()),                     # 刷新

    path('floors/',FloorListView.as_view()),                         # 获取所有楼层
    path('hostel/<int:floor_id>/',HostelListView.as_view()),         # 获取单个楼层的所有宿舍信息
    path('students/',StudentListView.as_view()),                     # 获取所有学生
    path('teachers/',TeacherListView.as_view()),                     # 获取所有老师

    path('create/floor/',CreateFloorView.as_view()),                 # 创建楼层
    path('delete/<int:pk>/floor',FloorDeleteView.as_view()),         # 删除楼层

    path('create/hostel/',CreateHostelView.as_view()),               # 创建宿舍
    path('delete/<int:pk>/hostel/',HostelDeleteView.as_view()),      # 删除宿舍

    path('delete/fromhostel/student/',DeleteStudentFromHostelView.as_view()),            # 从宿舍中删除学生
    path('add/fromhostel/student/',AssignStudentToHostelView.as_view()),                 # 为学生分配宿舍

    path('craete/teacher/',CreateUserView.as_view()),                # 创建用户（老师）
    path('delete/<int:pk>/teacher',DeleteTeacherView.as_view()),     # 禁用老师账号
    path('restore/<int:pk>/teacher',RestoreTeacherView.as_view()),   # 恢复老师账号
    path('delete/permanently/<int:pk>/teacher',DeleteTeacherPermanentlyView.as_view()),  # 彻底删除老师账号

    path('add/hostel/manager/', AddManagerToHostelView.as_view()),   # 添加宿舍管理员

    path('getall/hostellogs', GetAllHostelLogsView.as_view()),       # 获取所有宿舍申请记录

    # 门禁卡管理
    path('card/all/',GetAllCardsView.as_view()),                     # 获取所有门禁卡
    path('card/creates/',CreateCardsView.as_view()),                 # 创建门禁卡
    path('card/update/manager',UpdateCardsManagerView.as_view()),    # 跟新门禁管理员
    path('card/delete/',DeleteCardView.as_view())                   # 删除门禁卡
]