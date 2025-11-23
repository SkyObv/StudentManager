from users.models import Student
from rest_framework.generics import ListAPIView
from .serializers import StudentListViewSerializer

# Create your views here.
# 获取所有学生
class StudentListView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentListViewSerializer
