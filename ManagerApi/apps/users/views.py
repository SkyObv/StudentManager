from django.shortcuts import render
from django.template.context_processors import request
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import CustomTokenObtainPairSerializer, GetAllStudentsSerializer,FloorSerializer,HostelStudentSerializer
from rest_framework.generics import ListAPIView
from .models import User, Floor, Hostel
from .filters import StudentFilter


# 重写登入视图
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# 获取所有学生
class StudentListView(ListAPIView):
    queryset = User.objects.filter(user_type='student')
    serializer_class = GetAllStudentsSerializer
    filterset_class = StudentFilter
    # (可选) 指定可以进行排序的字段，这会增加 API 的灵活性
    ordering_fields = ['id', 'house_number__hostel_number']

# 获取所有楼层
class FloorListView(ListAPIView):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    pagination_class = None

# 获取单个楼层的所有宿舍信息
class HostelListView(ListAPIView):
    serializer_class = HostelStudentSerializer
    def get_queryset(self):
        floor_id = self.kwargs.get('floor_id')
        return Hostel.objects.filter(floor_id=floor_id)