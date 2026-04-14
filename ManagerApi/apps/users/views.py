import json

from django.http import Http404
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import (CustomTokenObtainPairSerializer, GetAllStudentsSerializer,FloorSerializer,
                         HostelStudentSerializer, CreateHostelViewSerializer, GetAllTeachersSerializer,
                         CreateUserSerializer, GetAllHostelLogsSerializer,GetAllCardsSerializer,CreateAllCardsSerializer,
                         UpdateCardsManagerSerializer)
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, Floor, Hostel
from .filters import StudentFilter, HostelFilter, TeachersFilter, TripsLogLogsFilter
from django.db import transaction # 导入事务
from teacher.models import HostelApply,TripsLog
from teacher.permissions import IsAdmin
from rest_framework_simplejwt.authentication import JWTAuthentication                    # 导入JWT认证
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import socket


# 重写登入视图
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# 获取所有学生视图
class StudentListView(ListAPIView):
    queryset = User.objects.filter(user_type='student')
    serializer_class = GetAllStudentsSerializer
    filterset_class = StudentFilter
    # (可选) 指定可以进行排序的字段，这会增加 API 的灵活性
    ordering_fields = ['id', 'house_number__hostel_number']

# 获取所有老师信息
class TeacherListView(ListAPIView):
    queryset = User.objects.filter(user_type='teacher')
    serializer_class = GetAllTeachersSerializer
    filterset_class = TeachersFilter
    ordering_fields = ['id']
    pagination_class = None

# 获取所有楼层视图
class FloorListView(ListAPIView):
    queryset = Floor.objects.filter(is_deleted=False)
    serializer_class = FloorSerializer
    pagination_class = None

# 获取单个楼层的所有宿舍信息视图
class HostelListView(ListAPIView):
    serializer_class = HostelStudentSerializer
    filterset_class = HostelFilter
    def get_queryset(self):
        floor_id = self.kwargs.get('floor_id')
        return Hostel.objects.filter(floor_id=floor_id,is_deleted=False)

# 创建楼层视图
class CreateFloorView(APIView):
    # 添加权限控制
    # permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        floor_name = request.data.get('floor_name')
        # 基础验证
        if not floor_name:
            return Response(
                {"message": "楼层名称不能为空。"},
                status=400
            )
        try:
            # 使用事务保证操作的原子性
            with transaction.atomic():
                # 尝试获取楼层（无论是否被删除），并使用 select_for_update 锁定该行,这可以防止在高并发时出现竞态条件
                floor = Floor.objects.select_for_update().get(floor_name=floor_name)
                # 如果能获取到，说明楼层已存在
                if floor.is_deleted:
                    floor.is_deleted = False
                    floor.save()
                    return Response(
                        {"message": "楼层已成功恢复。"},
                        status=201
                    )
                else:
                    return Response(
                        {"message": "该楼层已存在。"},
                        status=400
                    )
        except Floor.DoesNotExist:
            # 创建新楼层
            with transaction.atomic():
                Floor.objects.create(floor_name=floor_name)
                return Response(
                    {"message": "楼层已成功创建。"},
                    status=201
                )
# 删除楼层视图
class FloorDeleteView(DestroyAPIView):
    queryset = Floor.objects.filter(is_deleted=False)

    # 重写销毁方法
    def delete(self, request, *args, **kwargs):
        # 从 URL 中获取楼层 ID
        floor_id = kwargs.get('pk')
        try:
            # 使用事务确保操作的原子性
            with transaction.atomic():
                # 获取要删除的楼层实例
                instance = Floor.objects.get(id=floor_id, is_deleted=False)
                # 软删除该楼层下的所有宿舍，并获取更新的数量
                updated_hostels_count = instance.hostels.all().update(is_deleted=True)
                # 软删除楼层本身
                instance.is_deleted = True
                instance.save()
                response_data = {
                    'message': f'楼层 "{instance.floor_name}" 已成功删除。',
                    'deleted_hostels_count': updated_hostels_count
                }
                return Response(response_data, status=200)
        except Floor.DoesNotExist:
            return Response(
                {"message": "未找到指定的楼层或该楼层已被删除。"},
                status=404
            )

# 创建宿舍视图
class CreateHostelView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateHostelViewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status = 201,)
# 删除宿舍
class HostelDeleteView(DestroyAPIView):
    queryset = Hostel.objects.filter(is_deleted=False)
    # 第一种 分步重写
    def perform_destroy(self, instance):
        """
        删除逻辑 instance为查询出的对象
        """
        # 软删除宿舍
        instance.is_deleted = True
        instance.students_house.clear()
        instance.save()

    def delete(self, request, *args, **kwargs):
        """
        覆盖 delete 方法以返回自定义的成功消息。
        """
        with transaction.atomic():
            # 它会在这个 queryset (Hostel.objects.filter(is_deleted=False)) 中查找 pk 匹配的对象
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {'message': f'宿舍 "{instance.hostel_number}" 已成功删除。'},
                status=200,
            )
    # 第二种 重写销毁方法
    # def delete(self, request, *args, **kwargs):
    #     hostel_id = kwargs.get('pk')                                 # 获取删除宿舍 ID
    #     try:
    #         with transaction.atomic():
    #             instance = Hostel.objects.get(id=hostel_id, is_deleted=False)
    #             instance.is_deleted = True
    #             instance.save()
    #             response_data = {
    #                 'message': f'宿舍 "{instance.hostel_number}" 已成功删除。'
    #             }
    #             return Response(response_data, status=200)
    #     except Hostel.DoesNotExist:
    #         return Response(
    #             {"message": "未找到指定的宿舍或该宿舍已被删除。"},
    #         )

# 从宿舍中删除学生
class DeleteStudentFromHostelView(APIView):
    def delete(self, request, *args, **kwargs):
        try:
            student_obj = User.objects.get(
                username=request.query_params.get('username'),
                user_type='student',
                is_active=True,
            )
            if student_obj.house_number:
                student_obj.house_number = None
                student_obj.save(update_fields=['house_number'])
                return Response(
                    {"message": "学生已从宿舍中删除。"},
                    status=200
                )
            return Response(
                {"message": "该学生未加入宿舍。"},
                status=400
            )
        except User.DoesNotExist:
            return Response(
                {"message": "未找到指定的学生。"},
                status=404
            )
# 为学生分配宿舍
class AssignStudentToHostelView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        hostel_id = request.data.get('hostel_id')
        try:
            student_obj = User.objects.get(
                username=username,
                user_type='student',
                is_active=True,
            )
            student_obj.house_number = Hostel.objects.get(id=hostel_id)
            student_obj.save(update_fields=['house_number'])
            return Response(
                {
                    "message": "学生已分配宿舍。",
                    "username": username,
                    "hostel_id": hostel_id
                },
                status=200
            )
        except Exception as e:
            return Response(
                {
                    "message": "未找到指定的学生。",
                },
                status=404
            )

# 创建用户账号
class CreateUserView(CreateAPIView):
    serializer_class = CreateUserSerializer
# 禁用老师账号
class DeleteTeacherView(APIView):
    def delete(self, request, *args, **kwargs):
        teacher_id = kwargs.get('pk')
        try:
            with transaction.atomic():
                teacher_obj = User.objects.get(
                    id=teacher_id,
                    user_type='teacher',
                    is_active=True,
                )
                teacher_obj.is_active = False
                teacher_obj.save(update_fields=['is_active'])
            return Response(
                {
                    "message": "老师已禁用。",
                    "teacher_id": teacher_id
                },
                status=200
            )
        except User.DoesNotExist:
            return Response(
                {
                    "message": "未找到指定的老师。",
                },
                status=404
            )
# 恢复老师账号
class RestoreTeacherView(APIView):
    def post(self, request, *args, **kwargs):
        teacher_id = kwargs.get('pk')
        print(teacher_id)
        try:
            with transaction.atomic():
                teacher_obj = User.objects.get(
                    id=teacher_id,
                    user_type='teacher',
                    is_active=False,
                )
                teacher_obj.is_active = True
                teacher_obj.save(update_fields=['is_active'])
            return Response(
                {
                    "message": "老师已恢复。",
                    "teacher_id": teacher_id
                },
                status=200
            )
        except User.DoesNotExist:
            return Response(
                {
                    "message": "未找到指定的老师。",
                },
                status=404
            )
# 彻底删除老师账号
class DeleteTeacherPermanentlyView(APIView):
    def delete(self, request, *args, **kwargs):
        teacher_id = kwargs.get('pk')
        try:
            with transaction.atomic():
                teacher_obj = User.objects.get(
                    id=teacher_id,
                    user_type='teacher',
                )
                teacher_obj.delete()
            return Response(
                {
                    "message": "老师已彻底删除。",
                    "teacher_id": teacher_id
                },
                status=200
            )
        except User.DoesNotExist:
            return Response(
                {
                    "message": "未找到指定的老师。",
                },
            )

# 添加宿舍管理员
class AddManagerToHostelView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        hostel_id = request.data.get('hostel_id')
        try:
            hostel_obj = Hostel.objects.get(id=hostel_id)
            manager = User.objects.get(
                username=username,
                user_type='teacher',
                is_active=True,
            )
            hostel_obj.manager = manager
            manager = manager.last_name + manager.first_name
            hostel_obj.save(update_fields=['manager'])
            return Response(
                {
                    "message": "宿舍管理员已添加。",
                    "manager": manager,
                    "hostel_id": hostel_id
                },
                status=200
            )
        except Hostel.DoesNotExist:
            return Response(
                {
                    "message": "未找到指定的宿舍。",
                },
                status=404
            )
    def delete(self, request, *args, **kwargs):
        hostel_id = request.query_params.get('pk')
        try:
            hostel_obj = Hostel.objects.get(id=hostel_id)
            hostel_obj.manager = None
            hostel_obj.save(update_fields=['manager'])
            return Response(
                {
                    "message": "宿舍管理员已删除。",
                    "hostel_id": hostel_id
                },
                status=200
            )
        except Hostel.DoesNotExist:
            return Response(
                {
                    "message": "未找到指定的宿舍。",
                },
                status=404
            )

# 获取所有宿舍申请记录
class GetAllHostelLogsView(ListAPIView):
    queryset = HostelApply.objects.select_related(
        'teacher',           # 使用字段名，不是模型名
        'hostel__floor'      # 预加载宿舍及其楼层
    ).filter(apply_state="待审核")
    serializer_class = GetAllHostelLogsSerializer
    pagination_class = None
    ordering = ('-created_at',)

"""门禁卡管理"""
# 获取所有门禁卡
class GetAllCardsView(ListAPIView):
    queryset = TripsLog.objects.select_related(
        'manager_teacher',
        'student',
    ).all()
    serializer_class = GetAllCardsSerializer
    filterset_class = TripsLogLogsFilter
# 添加门禁卡(可批量添加)
class CreateCardsView(CreateAPIView):
    queryset = TripsLog.objects.all()
    serializer_class = CreateAllCardsSerializer
    authentication_classes = [JWTAuthentication]                               # 登入JWT认证
    permission_classes = [IsAuthenticated, IsAdmin]                            # 必须是登入用户和老师身份
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,many=True)            # 列表批量创建
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)  # 默认返回资源URL头
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
# 批量更新门禁卡管理员
class UpdateCardsManagerView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdmin]
    def post(self, request, *args, **kwargs):
        card_ids = request.data.get('card_ids', [])
        teacher_id = request.data.get('teacher_id')
        if not card_ids or not isinstance(card_ids, list):
            return Response({"error": "card_ids 必须是一个非空列表"}, status=status.HTTP_400_BAD_REQUEST)
        if not teacher_id:
            return Response({"error": "teacher_id 不能为空"}, status=status.HTTP_400_BAD_REQUEST)
        teacher_obj = User.objects.get(id=teacher_id)
        teacher_id = teacher_obj.id
        updated_count = TripsLog.objects.filter(id__in=card_ids).update(manager_teacher=teacher_id)
        return Response({
            "message": f"成功更新 {updated_count} 张门禁卡的管理员",
        }, status=status.HTTP_200_OK)
# 删除门禁卡
class DeleteCardView(DestroyAPIView):
    queryset = TripsLog.objects.all()
    serializer_class = GetAllCardsSerializer
    permission_classes = [IsAuthenticated,IsAdmin]
    authentication_classes = [JWTAuthentication]
    def get_object(self):
        card_id = self.request.query_params.get('card_id')
        if not card_id:
            raise Http404
        obj = self.queryset.get(id=card_id)
        return obj
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "门禁卡删除成功"}, status=status.HTTP_200_OK)

"""硬件控制"""
# led开灯
class OpenLedView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated,IsAdmin]
    def post(self, request, *args, **kwargs):
        data = request.data
        host_id = data.get('hostel_id')                                        # 操作宿舍列表
        instruction = data.get('instruction')                                  # 操作指令
        if host_id == "all":
            all_hostels = Hostel.objects.filter(is_active=True)
            # all_hostels.update(led_status=instruction)                       # 更新状态
        else:
            all_hostels = Hostel.objects.filter(id__in=host_id)
            gpio = all_hostels.first().led_GPIO
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              # 创建客户端嵌套字
            s.connect(('10.118.140.203', 8080))
            data = {
                "GPIO": gpio,
                "value": 1 if instruction else 0,
            }
            s.send(bytes(json.dumps(data), 'utf-8'))                           # 开灯
            all_hostels.update(led_status=instruction)                         # 更新状态
        return Response("ok", status=status.HTTP_200_OK)

