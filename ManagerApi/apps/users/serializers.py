# 自定义序列化器
# 添加自定义字段到token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User, AdminOptions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

# 自定义登入序列化器
class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    identity = serializers.CharField(write_only=True, required=True)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 添加自定义字段
        token['name'] = user.name                                    # 姓名
        token['identity'] = user.identity                            # 身份

        return token

    def validate(self, attrs):
        username = attrs.get('username')                             # 用户名
        password = attrs.get('password')                             # 密码
        identity = attrs.get('identity')                             # 身份

        try:
            # 同时验证用户名和角色，确保用户以正确的身份登录
            user = User.objects.get(username=username, identity=identity)
        except User.DoesNotExist:
            raise AuthenticationFailed('用户名、密码或角色不匹配。')

        # 验证密码
        if not user.check_password(password):
            raise AuthenticationFailed('用户名、密码或角色不匹配。')

        # 创建refresh token
        refresh = RefreshToken.for_user(user)

        # 返回数据
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'name': user.name,
            'identity': user.identity
        }
        return data

# 管理员视图序列化器
class AdminOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminOptions
        fields = ['options']
