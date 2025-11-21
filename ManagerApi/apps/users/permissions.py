# 权限类
from rest_framework.permissions import BasePermission
from .models import User

class IsStudent(BasePermission):
    """
    只允许学生身份的用户访问
    """
    def has_permission(self, request, view):
        # 1. 首先判断用户是否已认证
        # 2. 然后判断用户的身份是否是 'student'
        return request.user.is_authenticated and request.user.identity == User.IDENTITY_STUDENT

class IsTeacher(BasePermission):
    """
    只允许教师身份的用户访问
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.identity == User.IDENTITY_TEACHER

class IsAdmin(BasePermission):
    """
    只允许管理员身份的用户访问
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.identity == User.IDENTITY_ADMIN
