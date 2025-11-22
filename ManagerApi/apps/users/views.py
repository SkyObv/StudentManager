from django.shortcuts import render
from .serializers import CustomTokenObtainSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.
# 自定义登入视图
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer