from django.test import TestCase
import pandas

def craete_student(file_xlsx):
    df = pandas.read_excel(file_xlsx, header=0, dtype=str)
    print(df.columns)
    for i in range(len(df)):
        user = df.loc[i].to_dict()
        print( user)
        return "成功"


if __name__ == '__main__':
    path = r"D:\pyProject\StudenManager\测试导入文件数据\student_test_data.xlsx"
    craete_student(path)

