import pandas
import numpy
import django
from teacher.serializer import FileFieldSerializer
from users.models import User


"""
    file_path 导入的文件路径
"""
def export_student(file_path,teacher):
    column_dict = {
        '学号':'username',
        '姓':'first_name',
        '名':'second_name',
        '性别':'gender',
        '指导老师':'teacher_id'
    }
    # header=0 已经把第一行变成了列名，剩下的都是纯数据
    df = pandas.read_excel(file_path, header=0, dtype=str)
    df = df.rename(columns=column_dict)                                        # 重命名列
    student_list = df.to_dict('records')                                       # 返回一个 包含字典的列表
    return student_list

if __name__ == '__main__':
    django.setup()
    student_dict = export_student(r'E:\pythonproject\students-manager\测试导入文件数据\测试数据.xlsx')
    serializer = FileFieldSerializer(student_dict, many=True)
    print(serializer.data)
