from rest_framework.permissions import BasePermission
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Student, Teacher


class IsStudent(BasePermission):
    """
    只允许学生身份的用户访问
    """

    def has_permission(self, request, view):
        # 1. 首先判断用户是否已认证
        if not request.user or not request.user.is_authenticated:
            return False

        # 2. 尝试在 Student 表中查找与当前用户名相同的记录
        try:
            Student.objects.get(username=request.user.username)
            return True  # 找到了，说明是学生
        except ObjectDoesNotExist:
            return False  # 没找到，说明不是学生


class IsTeacher(BasePermission):
    """
    只允许教师身份的用户访问
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            Teacher.objects.get(username=request.user.username)
            return True
        except ObjectDoesNotExist:
            return False


class IsAdmin(BasePermission):
    """
    只允许管理员身份的用户访问
    """

    def has_permission(self, request, view):
        # 管理员是 AUTH_USER_MODEL (User) 的实例，并且拥有管理员权限
        # 我们可以直接检查 is_staff 和 is_superuser
        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.is_staff or request.user.is_superuser