from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from users.models import User,Floor,Hostel
from .models import HostelApply,TripsLog
from django.db import transaction  # 引入事务

# 获取老师所有学生序列化器
class GetAllStudentsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    house_number = serializers.SerializerMethodField()
    key_number = serializers.SerializerMethodField()
    key_state = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'gender','user_type','house_number','key_number','key_state']
    def get_name(self, obj):
        return obj.last_name + obj.first_name
    def get_house_number(self, obj):
        if obj.house_number:
            house_number = obj.house_number.floor.floor_name + '-' + obj.house_number.hostel_number
            return house_number
        return "无"
    def get_key_number(self, obj):
        if hasattr(obj, 'key'):
            return obj.key.number
        return '未绑定'
    def get_key_state(self, obj):
        if hasattr(obj, 'key'):
            return obj.key.key_card_state
        return '未绑定'
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
    def create(self, validated_data):
        """批量创建用户"""
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

# 我的宿舍
# 获取围殴的宿舍学生信息
class GetMyStudent(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','name','username','gender']
    def get_name(self, obj):
        return obj.last_name + obj.first_name
# 获取我的所有宿舍信息
class GetAllMyHostelSerializer(serializers.ModelSerializer):
    students = GetMyStudent(
        source='students_house',
        many=True
    )
    floor = serializers.SerializerMethodField()
    class Meta:
        model = Hostel
        fields = ['id','floor','hostel_number','gender','students']
    def get_floor(self, obj):
        return obj.floor.floor_name
# 从宿舍中删除学生
class DeleteStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','house_number']
    def update(self, instance, validated_data):
        instance.house_number = None
        instance.save()
        return instance
# 添加学生到宿舍
class AddStudentSerializer(serializers.Serializer):
    hostel_id = serializers.IntegerField()
    student_ids = serializers.ListField(child=serializers.IntegerField())
    def validate_hostel_id(self, value):
        try:
            hostel = Hostel.objects.get(id=value)
        except Hostel.DoesNotExist:
            raise serializers.ValidationError("宿舍不存在")
        request = self.context.get('request')
        user = request.user
        if hostel.manager != user:
                raise serializers.ValidationError("您无权操作此宿舍")
        return hostel
    def validate_student_ids(self, value):
        request = self.context.get('request')
        user = request.user
        students = User.objects.filter(id__in=value,teacher_id=user.id)
        if students.count() != len(value):
            raise serializers.ValidationError("部分学生不存在")
        return students
    def validate(self, data):
        hostel = data['hostel_id']
        students = data['student_ids']
        student_count = hostel.student_count + students.count()
        if student_count > 6:
            raise serializers.ValidationError("宿舍人数超过限制")
        return data
    def save(self, **kwargs):
        hostel = self.validated_data['hostel_id']
        students = self.validated_data['student_ids']
        with transaction.atomic():
            update_count = students.update(house_number=hostel)
            return {
                "messgae": "修改成功",
                "count": update_count,
            }

# 门禁卡管理
# 获取所有门禁卡
class ManagerTeacherSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','name','user_type','is_active']
    def get_name(self, obj):
        return obj.last_name + obj.first_name
class StudentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','name','username','gender']
    def get_name(self, obj):
        return obj.last_name + obj.first_name
class GetAllTripsSerializer(serializers.ModelSerializer):
    manager_teacher = ManagerTeacherSerializer(read_only=True)
    student = StudentSerializer(read_only=True)
    class Meta:
        model = TripsLog
        fields = ['id','number','manager_teacher','in_hostel','update_time','create_time','key_card_state','student']
class UpdateTripsSerializer(serializers.ModelSerializer):
    manager_teacher = ManagerTeacherSerializer(read_only=True)
    student = StudentSerializer(read_only=True)
    class Meta:
        model = TripsLog
        fields = ['id','number','manager_teacher','in_hostel','update_time','create_time','key_card_state','student']
class A(serializers.ModelSerializer):
    class Meta:
        model = TripsLog
        fields = '__all__'