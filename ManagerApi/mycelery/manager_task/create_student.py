from teacher.serializer import FileFieldSerializer
import pandas
from ..main import app
import os

@app.task(name="craete_student",bind=True)
def create_student(self, file_xlsx):
    result = {}                                                      # 结果列表
    ok_student = []                                                  # 成功的数据
    err_student = []                                                 # 失败的数据
    df = pandas.read_excel(file_xlsx, header=0, dtype=str)
    for i in range(len(df)):
        user = df.loc[i].to_dict()
        user = {
            "username": user['学号'],
            "last_name": user['姓'],
            "first_name": user['名'],
            "gender": user['性别'],
            "teacher": user['指导老师'],
        }
        ser = FileFieldSerializer(data=user)
        if ser.is_valid():
            print(ser.validated_data)
            ser.save()
            ok_student.append(user)
        else:
            err_student.append(user)
    result['ok_count'] = len(ok_student)
    result['err_count'] = len(err_student)
    result['ok_student'] = ok_student
    result['err_student'] = err_student
    os.remove(file_xlsx)
    return result