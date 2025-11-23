from rest_framework.serializers import ModelSerializer
from users.models import Student, Teacher, ClassBan

# 老师序列化器
class TeacherSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['name']  # 你想返回老师的哪些信息
# 班级序列化器
class ClassBanSerializer(ModelSerializer):
    teacher = TeacherSerializer(read_only=True)                      # 只返回数据
    class Meta:
        model = ClassBan
        fields = ['name', 'grade', 'teacher']

# 获取所有学生序列化器
class StudentListViewSerializer(ModelSerializer):
    class_ban = ClassBanSerializer(read_only=True)
    class Meta:
        model = Student
        fields = ['id','name','username','gender','is_active','class_ban']