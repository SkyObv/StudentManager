import django_filters
from django.db.models import Q

# 获取学生过滤器
class GetStudentFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_by_search',
        label="搜索"
    )
    gender = django_filters.CharFilter(field_name='gender', lookup_expr='iexact')

    # 搜索查找用户
    def filter_by_search(self, queryset, name, value):
        if value:
            # 搜索词条： 学号，宿舍门门牌号
            queryset = queryset.filter(
                Q(username__exact=value) | Q(house_number__hostel_number__exact=value)
            )
            return queryset
        return queryset
