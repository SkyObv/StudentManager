from .models import User,Floor,Hostel
from teacher.models import HostelApply,TripsLog
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator

# 自定义 JWT 认证返回结果
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    user_type = serializers.CharField(required=True)
    # 自定义返回数据
    def validate(self, attrs):
        res_user_type = attrs.get('user_type')
        data = super().validate(attrs)
        if self.user.user_type != res_user_type:
            raise AuthenticationFailed(
                detail=f'用户类型不匹配。',
            )
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
        fields = ['hostel_number','floor','student_count','is_full','gender']
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
        fields = ['id','username','name','gender']
    def get_name(self, obj):
        """获取学生的姓名"""
        return obj.last_name + obj.first_name
class HostelStudentSerializer(HostelSerializer):
    students = Hoste_StudentSerializer(
        source='students_house',                                     # students_house是我们在 User 模型中定义的 related_name,反向查询
        many=True,
        read_only=True
    )
    manager = serializers.SerializerMethodField()
    class Meta:
        model = Hostel
        fields = ['id','hostel_number','floor','student_count','is_full','gender','manager','students',
                  'led_GPIO','led_status']
    def get_manager(self, obj):
        """获取宿舍楼管理员"""
        if obj.manager:
            return f"{obj.manager.last_name}{obj.manager.first_name}"
        else:
            return None

# 宿舍楼信息序列化器
class FloorSerializer(serializers.ModelSerializer):
    # 房间总数
    rooms = serializers.SerializerMethodField()
    # 有人的房间数
    have_people_rooms = serializers.SerializerMethodField()
    # 宿舍信息获取
    class Meta:
        model = Floor
        fields = ['id','floor_name','rooms','have_people_rooms']
    def get_rooms(self, obj):
        """获取房间总数"""
        return obj.hostels.filter(is_deleted=False).count()
    def get_have_people_rooms(self, obj):
        """获取有人的房间数"""
        return obj.hostels.filter(
            is_deleted=False,
            students_house__isnull=False
        ).distinct().count()

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

# 获取所有老师序列化器
class GetAllTeachersSerializer(serializers.ModelSerializer):
    """获取所有教师"""
    name = serializers.SerializerMethodField()
    counts = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'gender', 'is_active', 'counts']
    def get_name(self, obj):
        """获取老师的姓名"""
        return obj.last_name + obj.first_name
    def get_counts(self, obj):
        """统计老师所有的学生"""
        return obj.students.filter(is_active=True).count()

# 创建宿舍序列化器
class CreateHostelViewSerializer(serializers.ModelSerializer):
    students = Hoste_StudentSerializer(
        source='students_house',  # students_house是我们在 User 模型中定义的 related_name,反向查询
        many=True,
        read_only=True
    )
    class Meta:
        model = Hostel
        fields = ['id','hostel_number','floor','student_count','is_full','gender','students']

    def validate(self, attrs):
        super().validate(attrs)
        # 判断宿舍在这个楼层内是否已存在
        floor_id = attrs['floor']                                    # 楼层 Floor 的主键
        hostel_number = attrs['hostel_number']                       # 需要创建的宿舍门牌号
        if Hostel.objects.filter(floor_id=floor_id, hostel_number=hostel_number,is_deleted=False).exists():
            raise serializers.ValidationError({'message': '该楼层已存在该宿舍。'})
        return attrs

# 创建用户账号序列化器
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'gender', 'user_type']
        extra_kwargs = {
            'id':{'required': False},
            'username': {'required': True},
            'password': {'required': True,'write_only': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'gender': {'required': True},
            'user_type': {'required': True}
        }
    def validate(self, attrs):
        super().validate(attrs)
        return attrs
    def create(self, validated_data):
        """创建用户"""
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # 关键：对密码进行哈希处理
        user.save()
        return user

# 获取所有宿舍申请记录序列化器
class GetAllHostelLogsSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()
    hostel = serializers.SerializerMethodField()
    class Meta:
        model = HostelApply
        fields = ['id','teacher','hostel','apply_state','apply_time']
    def get_teacher(self, obj):
        teacher = obj.teacher
        teacher_name = teacher.last_name + teacher.first_name
        return teacher_name
    def get_hostel(self, obj):
        hostel = obj.hostel
        hostel_name = hostel.floor.floor_name + '-' + hostel.hostel_number
        return hostel_name

"""门禁卡管理"""
# 获取我的所有门禁卡
class GetAllCardsSerializer(serializers.ModelSerializer):
    manager_teacher = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()
    class Meta:
        model = TripsLog
        fields = '__all__'
    def get_manager_teacher(self, obj):
        if not obj.manager_teacher:
            return None
        manager_teacher = {}
        manager_teacher['id'] = obj.manager_teacher.id
        manager_teacher['name'] = obj.manager_teacher.last_name + obj.manager_teacher.first_name
        manager_teacher['user_type'] = obj.manager_teacher.user_type
        manager_teacher['is_active'] = obj.manager_teacher.is_active
        return manager_teacher
    def get_student(self, obj):
        if not obj.student:
            return None
        student = {}
        student['id'] = obj.student.id
        student['name'] = obj.student.last_name + obj.student.first_name
        student['username'] = obj.student.username
        student['gender'] = obj.student.gender
        return student
# 创建门禁卡(可批量创建)
class CreateAllCardsSerializer(serializers.ModelSerializer):
    number = serializers.CharField(
        validators=[UniqueValidator(queryset=TripsLog.objects.all(), message="该卡号已存在")]
    )
    class Meta:
        model = TripsLog
        fields = '__all__'
# 批量更新门禁管理员
class UpdateCardsManagerSerializer(serializers.ModelSerializer):
    cards = serializers.SerializerMethodField()
    teacher = serializers.SerializerMethodField()
    class Meta:
        model = TripsLog
        fields = '__all__'