from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainSerializer

# Create your views here.
# 自定义登入视图
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer