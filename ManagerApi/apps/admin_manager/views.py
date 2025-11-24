from users.models import Student, ClassBan
from rest_framework.generics import ListAPIView, UpdateAPIView
from .serializers import StudentListViewSerializer, StudentUpdateSerializer, ClassBanSerializer

# Create your views here.
# 条件所有学生
class StudentListView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentListViewSerializer
    ordering = ['id']                                                # 默认排序字段

    def get_queryset(self):
        queryset = super().get_queryset()
        # 获取查询参数
        class_ban = self.request.query_params.get('class_ban')       # 班级
        grade = self.request.query_params.get('grade')               # 年级
        name = self.request.query_params.get('name')                 # 姓名
        username = self.request.query_params.get('username')         # 学号
        if class_ban:
            queryset = queryset.filter(class_ban=class_ban)
        if grade:
            queryset = queryset.filter(class_ban__grade=grade)
        if name:
            queryset = queryset.filter(name__icontains=name)
        if username:
            queryset = queryset.filter(username__icontains=username)

        return queryset

# 获取所有班级
class ClassBanListView(ListAPIView):
    queryset = ClassBan.objects.all()
    serializer_class = ClassBanSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # 获取查询参数
        grade = self.request.query_params.get('grade')               # 年级
        if grade:
            queryset = queryset.filter(grade=grade)
        return queryset


# 修改学生信息
class StudentUpdateView(UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentUpdateSerializer

