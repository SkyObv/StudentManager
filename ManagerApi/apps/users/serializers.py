# 自定义序列化器
# 添加自定义字段到token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User, Student, Teacher
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.backends import BaseBackend

# 自定义后端认证
class MultiModelAuthBackend(BaseBackend):
    """
    自定义认证后端，支持从多个用户模型中进行认证。
    """
    def authenticate(self, request, username=None, password=None, user_type=None, **kwargs):
        if user_type is None:
            return None
        # 根据 user_type 选择对应的模型
        user_model = None
        if user_type == 'admins':
            user_model = User
        elif user_type == 'student':
            user_model = Student
        elif user_type == 'teacher':
            user_model = Teacher
        else:
            return None  # 无效的用户类型
        try:
            # 从选定的模型中查找用户
            user = user_model.objects.get(username=username)
            # 检查密码是否正确
            if user.check_password(password) and user.is_active:
                return user
        except user_model.DoesNotExist:
            # 用户不存在
            return None
        return None

    def get_user(self, user_id):
        """
        根据 user_id 获取用户对象
        """
        # 依次尝试从三个模型中查找
        for model in [User, Student, Teacher]:
            try:
                return model.objects.get(pk=user_id)
            except model.DoesNotExist:
                continue
        return None
# 自定义登入序列化器
class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    user_type = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        username = attrs.get('username')                             # 用户名
        password = attrs.get('password')                             # 密码
        user_type = attrs.pop('user_type', None)                        # 身份

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password,
            user_type=user_type
        )

        if not user:
            raise AuthenticationFailed('用户名、密码或用户类型不正确')

        # 创建refresh token
        refresh = RefreshToken.for_user(user)

        # 返回数据
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_type': user_type,  # 返回用户类型
            'name': user.name
        }
        return data
