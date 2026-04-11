import time
from teacher.serializer import FileFieldSerializer
from users.models import User
from rest_framework import serializers
import pandas
from ..main import app
import os

# @app.task(name="craete_student")
# def create_student(file_xlsx):
#     result = {}                                                                          # 结果列表
#     ok_count = 0                                                                         # 成功的个数
#     err_count = 0                                                                        # 失败的个数
#     ok_student = []                                                                      # 成功的数据
#     err_student = []                                                                     # 失败的数据
#     try:
#         df = pandas.read_excel(file_xlsx, header=0, dtype=str)
#         df = handle_xlsx(df)                                                             # 数据处理
#         for i in range(len(df)):
#             user = df.loc[i].to_dict()
#             serializer = FileFieldSerializer(data=user)
#             if serializer.is_valid():
#                 serializer.save()
#                 ok_count += 1
#                 ok_student.append(user)
#             else:
#                 err_count += 1
#                 err_dict = serializer.errors
#                 err_dict['name'] = user['first_name']+user['last_name']
#                 err_student.append(err_dict)
#         result = {
#             "ok_count": ok_count,
#             "err_count": err_count,
#             "ok_student": ok_student,
#             "err_student": err_student,
#             }
#         return result
#     except Exception as e:
#         raise serializers.ValidationError(f"处理文件时发生错误: {str(e)}")
#     finally:
#         os.remove(file_xlsx)
# # 数据处理
# def handle_xlsx(file_xlsx):
#     new_columns = {
#         "学号": "username",
#         "密码": "password",
#         "姓": "last_name",
#         "名": "first_name",
#         "性别": "gender",
#         "指导老师": "teacher_id",
#     }
#     file_xlsx.rename(columns=new_columns, inplace=True)
#     return file_xlsx

@app.task(name="text")
def text():
    users = User.objects.get(id=1)                                                  # 在celery中使用orm
    return {"users": users.user_type}

@app.task(name="craete_student")
def create_student(file_path,teacher):
    column_dict = {
        '学号':'username',
        '姓':'first_name',
        '名':'last_name',
        '性别':'gender',
        '指导老师':'teacher_id'
    }
    # header=0 已经把第一行变成了列名，剩下的都是纯数据
    df = pandas.read_excel(file_path, header=0, dtype=str)
    df = df.rename(columns=column_dict)                                        # 重命名列
    # 先删除所有学生
    teacher_obj = User.objects.get(id=teacher)
    teacher_obj.students.all().delete()
    student_list = df.to_dict('records')                                       # 返回一个 包含字典的列表
    serializer = FileFieldSerializer(
        data=student_list,
        many=True,
    )
    serializer.is_valid(raise_exception=True)                                  # 字段验证
    serializer.save()
    return serializer.data