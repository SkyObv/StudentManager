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
class FileFieldSerializer(serializers.ModelSerializer):
    teacher_id = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.filter(user_type='teacher'),                               # 限制只能选择用户类型为老师的用户
    )
    class Meta:
        model = User
        fields = ['username','password','last_name','first_name','user_type','gender','teacher_id']
        extra_kwargs = {
            'password':{'write_only': True,'default':'123456'},
            'user_type':{'default': 'student'},
        }
    def validate_username(self, value):
        """验证用户名是否已存在"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('用户名已存在。')
        return value
    def create(self, validated_data):
        """创建用户"""
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
