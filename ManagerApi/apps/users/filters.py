import django_filters
from .models import User,Hostel
from django.db.models import Q

# 学生过滤器
class StudentFilter(django_filters.FilterSet):
    # 按宿舍门牌号过滤
    house_number = django_filters.CharFilter(
        field_name='house_number__hostel_number',                    # 跨表查询到 Hostel 模型的 hostel_number 字段
        lookup_expr='iexact'                                         # 不区分大小写的精确匹配
    )
    # 按楼层过滤
    floor = django_filters.CharFilter(
        field_name='house_number__floor__floor_name',                # 跨表查询到 Floor 模型的 floor_name 字段
        lookup_expr='iexact'
    )
    # 按指导教师的id过滤
    teacher_id = django_filters.NumberFilter(
        field_name='teacher_id'                                      # User 模型上的 teacher_id 字段本身就指向了教师的 ID
    )
    # 老师名字过滤
    teacher_name = django_filters.CharFilter(
        method='filter_by_teacher_name'                              # 指定一个自定义方法名
    )
    # 是否有宿舍过滤
    has_house = django_filters.BooleanFilter(
        method='filter_by_has_house'
    )
    class Meta:
        model = User
        # 这里我们通过自定义字段来覆盖，所以 Meta.fields 可以留空或省略
        fields = []
    # 自定义teacher_name过滤方法
    def filter_by_teacher_name(self, queryset, name, value):
        """
        自定义过滤方法，用于同时搜索教师的 last_name 和 first_name
        """
        # 如果前端没有提供搜索值，则直接返回原始查询集
        if not value:
            return queryset
        # 使用 Q 对象构建一个 OR 查询
        # icontains不区分大小写且包含匹配
        queryset = queryset.filter(
            Q(teacher_id__last_name__icontains=value) | Q(teacher_id__first_name__icontains=value)
        )
        return queryset
    # 自定义has_house过滤方法
    def filter_by_has_house(self, queryset, name, value):
        if value:  # 如果 value 是 True
            # 查找 house_number 不为空的学生
            return queryset.filter(house_number__isnull=False)
        else:  # 如果 value 是 False
            # 查找 house_number 为空的学生
            return queryset.filter(house_number__isnull=True)

# 楼层宿舍过滤器
class HostelFilter(django_filters.FilterSet):
    hostel_number = django_filters.CharFilter(
        field_name='hostel_number',
        lookup_expr='iexact'
    )
    gender = django_filters.CharFilter(
        field_name='gender',
        lookup_expr='iexact'
    )
    class Meta:
        model = Hostel
        fields = ['hostel_number', 'gender']
