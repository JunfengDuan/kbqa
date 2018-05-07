# coding:utf-8
import datetime


# 读文件
def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    return data


def get_current_time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")