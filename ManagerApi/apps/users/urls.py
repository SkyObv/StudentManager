from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view()),             # 登入
    path('refresh/', TokenRefreshView.as_view()),                    # 刷新token

]