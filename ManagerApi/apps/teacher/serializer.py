from rest_framework import serializers
from users.models import User,Floor,Hostel
from .models import HostelApply
from django.db import transaction  # 引入事务

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

# 宿舍申请
# 获取可申请的宿舍列表
class GetDormitoryHostelSerializer(serializers.ModelSerializer):
    hostel_number = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()
    floor_name = serializers.SerializerMethodField()
    class Meta:
        model = Hostel
        fields = ['id', 'hostel_number','gender','floor_name','student_count']
    def get_hostel_number(self, obj):
        return obj.floor.floor_name + '-' + obj.hostel_number
    def get_floor_name(self, obj):
        return obj.floor.floor_name
    def get_student_count(self, obj):
        return obj.student_count
# 申请宿舍
class CreateHostelApplyViewSerializer(serializers.ModelSerializer):
    hostel = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Hostel.objects.filter(is_deleted=False,manager__isnull=True),
    )
    class Meta:
        model = HostelApply
        fields = ['hostel']
    def validate(self, attrs):
        super().validate(attrs)
        request = self.context.get('request')
        teacher = request.user
        if HostelApply.objects.filter(teacher=teacher, hostel=attrs['hostel']).exists():
            raise serializers.ValidationError("您已申请过该宿舍，请勿重复提交。")
        return attrs

# 申请记录
# 获取所有申请记录
class GetAllApplySerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField()
    hostel_name = serializers.SerializerMethodField()
    class Meta:
        model = HostelApply
        fields = ['id','teacher_name','hostel_name','apply_time','apply_state']
    def get_teacher_name(self, obj):
        teacher = obj.teacher
        teacher_name = teacher.last_name + teacher.first_name
        return teacher_name
    def get_hostel_name(self, obj):
        hostel_name = obj.hostel.floor.floor_name + '-' + obj.hostel.hostel_number
        return hostel_name
# 管理员更新记录
class UpdateApplyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostelApply
        fields = ['id','apply_state']
    # 如果为通过给老师关联宿舍外键
    def update(self, instance, validated_data):
        with transaction.atomic():
            # 更新申请记录的状态
            instance = super().update(instance, validated_data)
            # 判断状态是否为"通过"
            if instance.apply_state == '通过':
                # 获取关联的宿舍对象
                hostel = instance.hostel
                # 将申请的老师设置为宿舍管理员
                hostel.manager = instance.teacher
                # x保存宿舍信息 (只更新 manager 字段，提高效率)
                hostel.save(update_fields=['manager'])
        return instance
# 删除申请记录
class DeleteApplyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostelApply
        fields = '__all__'