from rest_framework import permissions

# 自定义权限，只允许用户类型为 'teacher' 的用户访问。
class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        # 确保用户已认证
        if not request.user or not request.user.is_authenticated:
            return False
        # 检查用户的 user_type 是否为 'teacher'
        return request.user.user_type == 'teacher'