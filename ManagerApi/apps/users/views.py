from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import CustomTokenObtainPairSerializer, GetAllStudentsSerializer,FloorSerializer,HostelStudentSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Floor, Hostel
from .filters import StudentFilter
from django.db import transaction # 导入事务


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

# 获取所有楼层视图
class FloorListView(ListAPIView):
    queryset = Floor.objects.filter(is_deleted=False)
    serializer_class = FloorSerializer
    pagination_class = None

# 获取单个楼层的所有宿舍信息视图
class HostelListView(ListAPIView):
    queryset = Hostel.objects.filter(is_deleted=False)
    serializer_class = HostelStudentSerializer
    def get_queryset(self):
        floor_id = self.kwargs.get('floor_id')
        return Hostel.objects.filter(floor_id=floor_id)

# 创建楼层视图
class CreateFloorView(APIView):
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