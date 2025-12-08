from django.test import TestCase
from .serializer import FileFieldSerializer
import pandas

def craete_student(file_xlsx):
    # 定义列名映射字典
    column_mapping = {
        '学号': 'username',
        '姓': 'last_name',
        '名': 'first_name',
        '性别': 'gender',
        '指导老师': 'teacher'
    }
    df = pandas.read_excel(file_xlsx, header=0, dtype=str)
    # 清理列名（去除前后空格）
    df.columns = df.columns.str.strip()
    # 重命名列，使其与序列化器字段名匹配
    df = df.rename(columns=column_mapping)
    # 将空值替换为空字符串，避免后续处理出错
    df = df.fillna('')
    # 转换为字典列表
    students_data = df.to_dict('records')

    serializer = FileFieldSerializer(data=students_data, many=True)
    serializer.is_valid()
    print(students_data)

