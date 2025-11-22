from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView, AdminOptionsView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view()),             # 登入
    path('refresh/', TokenRefreshView.as_view()),                    # 刷新token

    path('admin/optins/', AdminOptionsView.as_view()),               # 管理员选项

]