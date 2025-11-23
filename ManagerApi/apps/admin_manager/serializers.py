from rest_framework.serializers import ModelSerializer
from users.models import Student

# 获取所有学生序列化器
class StudentListViewSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ['name','username','is_active']