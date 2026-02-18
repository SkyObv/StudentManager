import django_filters
from django.db.models import Q
from users.models import User,Floor,Hostel


# 获取学生过滤器
class GetStudentFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_by_search',
        label="搜索"
    )
    gender = django_filters.CharFilter(field_name='gender', lookup_expr='iexact')
    is_hostel = django_filters.BooleanFilter(
        method='filter_by_is_hostel',
        label="是否拥有宿舍"
    )
    # 搜索查找用户
    def filter_by_search(self, queryset, name, value):
        if value:
            # 搜索词条： 学号，宿舍门门牌号
            queryset = queryset.filter(
                Q(username__exact=value) | Q(house_number__hostel_number__exact=value)
            )
            return queryset
        return queryset
    def filter_by_is_hostel(self, queryset, name, value):
        if value:                                                    # 有宿舍
            queryset = queryset.filter(
                house_number__isnull=False
            )
            return queryset
        else:                                                        # 没有宿舍
            queryset = queryset.filter(
                house_number__isnull=True
            )
            return queryset

# 获取可申请宿舍过滤器
class GetHostelFilter(django_filters.FilterSet):
    floor = django_filters.CharFilter(
        field_name='floor__floor_name',                                   # 跨表查询到 Floor 模型的 floor_name 字段
        lookup_expr='iexact'
    )

# 老师申请宿舍记录过滤器
class GetApplyFilter(django_filters.FilterSet):
    apply_state = django_filters.CharFilter(field_name='apply_state', lookup_expr='iexact')

# 我的宿舍过滤
class GetMyHostelFilter(django_filters.FilterSet):
    floor = django_filters.CharFilter(                       # 根据楼层过滤
        field_name='floor__floor_name',
        lookup_expr='iexact'
    )
    gender = django_filters.CharFilter(                      # 根据性别过滤
        field_name='gender',
        lookup_expr='iexact'
    )
    class Meta:
        model = Hostel
        fields = []
