from rest_framework import serializers
from users.models import User

# 获取老师所有学生序列化器
class GetAllStudentsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    house_number = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'gender', 'is_active','user_type','house_number']
    def get_name(self, obj):
        return obj.last_name + obj.first_name
    def get_house_number(self, obj):
        if obj.house_number:
            house_number = obj.house_number.floor.floor_name + '-' + obj.house_number.hostel_number
            return house_number
        return "无"

# 上传文件字段验证序列化器
class FileFieldSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20,source="学号")
    last_name = serializers.CharField(max_length=20, source="姓")
    first_name = serializers.CharField(max_length=20, source="名")
    gender = serializers.ChoiceField(choices=(('male','男'),('female','女')), source="性别")
    teacher = serializers.CharField(max_length=20, source="指导老师")
    def validate_username(self, value):
        user = User.objects.filter(username=value)
        if user.exists():
            raise serializers.ValidationError("用户已存在")
        return value
    def validate_teacher(self, value):
        teacher = User.objects.filter(username=value, user_type="teacher")
        if not teacher.exists():
            raise serializers.ValidationError("老师不存在或账号以停用")
        return value