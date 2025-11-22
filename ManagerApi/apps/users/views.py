from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import ListAPIView
from .serializers import CustomTokenObtainSerializer, AdminOptionsSerializer
from .models import AdminOptions

# Create your views here.
# 自定义登入视图
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer

# 管理员的登入选项视图
class AdminOptionsView(ListAPIView):
    queryset = AdminOptions.objects.all()
    serializer_class = AdminOptionsSerializer