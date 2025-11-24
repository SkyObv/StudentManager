from rest_framework import serializers
from users.models import Student, Teacher, ClassBan

# 老师序列化器
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['name']  # 你想返回老师的哪些信息
# 班级序列化器
class ClassBanSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)                      # 只返回数据
    class Meta:
        model = ClassBan
        fields = ['name', 'grade', 'teacher']

# 获取所有学生序列化器
class StudentListViewSerializer(serializers.ModelSerializer):
    class_ban = ClassBanSerializer(read_only=True)
    # 自定义字段数据
    is_active = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = ['id','name','username','gender','is_active','class_ban']
    # 自定义返回字段数据
    def get_is_active(self, obj):
        return "是" if obj.is_active else "否"


# 用于更新学生信息的序列化器
class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        # 需要更新的字段
        fields = ['name','gender','username','is_active','class_ban']