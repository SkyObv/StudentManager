import os
import random
import time
from django.conf import settings
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User,Floor,Hostel
from rest_framework_simplejwt.authentication import JWTAuthentication                    # 导入JWT认证
from rest_framework.permissions import IsAuthenticated                                   # 内置权限
from .models import HostelApply
from .permissions import IsTeacher,IsAdmin
from .filters import GetStudentFilter, GetApplyFilter, GetHostelFilter
from .serializer import (GetAllStudentsSerializer, FileFieldSerializer, GetDormitoryHostelSerializer,
                         CreateHostelApplyViewSerializer,GetAllApplySerializer,UpdateApplyViewSerializer
                         ,DeleteApplyViewSerializer)
from mycelery.manager_task.create_student import create_student

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
            # 将文件保存在本地
            time_head = int(time.time()* 1000000)
            rand_head = random.randint(1000, 9999)
            file_path = os.path.join(settings.MEDIA_ROOT, f"{time_head}"+"_"+f"{rand_head}"+file_xlsx.name)
            with open(file_path, 'wb') as f:
                for chunk in file_xlsx.chunks():
                    f.write(chunk)
            # 创建任务
            task = create_student.delay(file_path)
            return Response(
                {
                    "message": "任务创建成功",
                    "task_id": task.id,
                }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "请上传xlsx文件"}, status=status.HTTP_400_BAD_REQUEST)
# 获取任务结果
class GetTaskResultView(APIView):
    def get(self, request,task_id,*args, **kwargs):
        if not task_id:
            return Response({"error": "请提供任务ID"}, status=status.HTTP_400_BAD_REQUEST)
        task = create_student.AsyncResult(task_id)
        if task.state == 'PENDING':
            return Response({"message": "任务正在处理中"}, status=status.HTTP_200_OK)
        if task.state == 'FAILURE':
            return Response({"error": "任务处理失败"}, status=status.HTTP_400_BAD_REQUEST)
        if task.state == 'SUCCESS':
            result = task.result
            return Response(result, status=status.HTTP_200_OK)

# 宿舍申请
# 获取可申请的宿舍列表
class GetDormitoryListView(ListAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, IsTeacher]
    queryset = Hostel.objects.filter(is_deleted=False, manager__isnull=True)
    serializer_class = GetDormitoryHostelSerializer
    filterset_class = GetHostelFilter
    pagination_class = None
# 申请宿舍
class ApplyHostelView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]
    serializer_class = CreateHostelApplyViewSerializer

    def perform_create(self, serializer):
        serializer.save(
            teacher=self.request.user,
        )

# 申请记录
# 获取申请记录
class GetApplyRecordView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]
    serializer_class = GetAllApplySerializer
    filterset_class = GetApplyFilter
    pagination_class = None

    def get_queryset(self):
        teacher_id = self.request.user.id
        queryset = HostelApply.objects.filter(
            teacher_id=teacher_id,
        )
        return queryset
# 管理员修改申请记录
class ApplyRecordView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = HostelApply.objects.filter(apply_state="待审核")
    serializer_class = UpdateApplyViewSerializer
# 删除申请记录
class DeleteApplyRecordView(DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher, IsAdmin]
    queryset = HostelApply.objects.exclude(apply_state="待审核")             # 排除待审核记录
    serializer_class = DeleteApplyViewSerializer