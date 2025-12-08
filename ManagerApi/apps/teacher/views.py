from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication                    # 导入JWT认证
from rest_framework.permissions import IsAuthenticated                                   # 内置权限
from .permissions import IsTeacher
from .filters import GetStudentFilter
from .serializer import GetAllStudentsSerializer, FileFieldSerializer
from .tests import craete_student

# 获取所有学生
class GetStudentListView(ListAPIView):
    authentication_classes = [JWTAuthentication]                                         # 登入JWT认证
    permission_classes = [IsAuthenticated, IsTeacher]                                    # 必须是登入用户和老师身份
    serializer_class = GetAllStudentsSerializer
    filterset_class = GetStudentFilter
    pagination_class = None

    def get_queryset(self):
        """获取查询集"""
        teacher_id = self.request.user.id
        queryset = User.objects.filter(
            teacher_id=teacher_id,
            user_type='student',
            is_active=True,
        )
        return queryset

# 导入学生生成学生用户视图
class ImportStudentsView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, IsTeacher]
    serializer_class = FileFieldSerializer
    def post(self, request):
        file_xlsx = request.FILES.get('file')
        if not file_xlsx:
            return Response({"error": "请上传文件"}, status=status.HTTP_400_BAD_REQUEST)
        if file_xlsx.name.endswith('.xlsx'):
            craete_student(file_xlsx)
            return Response({"message": "导入成功,用户创建中"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "请上传xlsx文件"}, status=status.HTTP_400_BAD_REQUEST)



