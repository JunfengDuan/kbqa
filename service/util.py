# coding:utf-8


# 读文件
def read_file(path):
    with open(path, 'rt', encoding='utf-8') as f:
        data = f.read()
    return data
