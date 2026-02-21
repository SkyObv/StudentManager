import os
import random
import time
from typing import override
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
from .filters import GetStudentFilter, GetApplyFilter, GetHostelFilter,GetMyHostelFilter
from .serializer import (GetAllStudentsSerializer, FileFieldSerializer, GetDormitoryHostelSerializer,
                         CreateHostelApplyViewSerializer,GetAllApplySerializer,UpdateApplyViewSerializer
                         ,DeleteApplyViewSerializer, GetAllMyHostelSerializer, DeleteStudentSerializer
                         ,AddStudentSerializer)
from mycelery.manager_task.create_student import create_student
from django.db.models import Prefetch

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
    permission_classes = [IsAuthenticated]
    queryset = HostelApply.objects.all()
    serializer_class = DeleteApplyViewSerializer

# 我的宿舍
# 获取所有宿舍以及学生信息
class GetAllMyHostelView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]
    serializer_class = GetAllMyHostelSerializer
    filterset_class = GetMyHostelFilter
    pagination_class = None

    def get_queryset(self):
        teacher_id = self.request.user.id
        queryset = Hostel.objects.filter(
            manager=teacher_id,
            is_deleted=False
        ).select_related(
            'floor'                                   # 优化 obj.floor 的访问，一对一
        ).prefetch_related(
            # 'students_house',                       # 优化 obj.students_house.all() 的访问 一对多
            Prefetch(
                'students_house',
                queryset=User.objects.only('id', 'first_name', 'last_name', 'gender')
            )
        )
        return queryset
# 从宿舍中删除学生
class DeleteStudentView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]
    serializer_class = DeleteStudentSerializer
    @override
    def get_queryset(self):
        teacher = self.request.user
        return User.objects.filter(teacher_id=teacher.id)
    def get_object(self):
        pk = self.request.query_params.get('pk')
        queryset = self.get_queryset()
        obj = queryset.get(pk=pk)
        return obj
# 将学生添加到宿舍中
class AddStudentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]
    serializer_class = AddStudentSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        a = serializer.save()
        return Response(a,status=status.HTTP_200_OK)