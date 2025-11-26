from .models import User,Floor,Hostel
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

# 自定义 JWT 认证返回结果
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # 自定义返回数据
    def validate(self, attrs):
        data = super().validate(attrs)
        # 向响应中添加自定义数据
        data['user_type'] = self.user.user_type
        data['name'] = self.user.last_name + self.user.first_name
        return data

# 宿舍信息序列化器
class HostelSerializer(serializers.ModelSerializer):
    student_count = serializers.SerializerMethodField()              # 宿舍人数，虚拟字段，动态计算
    is_full = serializers.SerializerMethodField()                    # 宿舍是否已满，虚拟字段，动态计算
    class Meta:
        model = Hostel
        fields = ['hostel_number','floor','student_count','is_full']
    def get_student_count(self, obj):
        """获取宿舍人数"""
        return obj.student_count
    def get_is_full(self, obj):
        """判断宿舍是否已满"""
        return obj.is_full

# 宿舍信息学生序列化器
class Hoste_StudentSerializer(serializers.ModelSerializer):
    """获取宿舍学生信息"""
    name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'name']
    def get_name(self, obj):
        """获取学生的姓名"""
        return obj.last_name + obj.first_name
class HostelStudentSerializer(HostelSerializer):
    students = Hoste_StudentSerializer(
        source='students_house',                                     # students_house是我们在 User 模型中定义的 related_name,反向查询
        many=True,
        read_only=True
    )
    class Meta:
        model = Hostel
        fields = ['hostel_number','floor','student_count','is_full','students']

# 宿舍楼信息序列化器
class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = '__all__'

# 学生用户信息序列化器
class GetAllStudentsSerializer(serializers.ModelSerializer):
    """获取所有学生"""
    # 定义一个计算字段
    name = serializers.SerializerMethodField()
    house_number = HostelSerializer()                                # 宿舍信息,嵌套序列化器
    # 使用 StringRelatedField
    teacher_id = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'name', 'user_type','teacher_id', 'house_number']   # 需要序列化的字段

    def get_name(self, obj):
        """获取学生的姓名"""
        return obj.last_name + obj.first_name