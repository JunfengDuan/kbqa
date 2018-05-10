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


def get_kblabels():
    kb_labels = [['Cadre', 'Cadre_Province', 'Province'],
                 ['Cadre', 'Cadre_City', 'City'],
                 ['Cadre', 'Cadre_District', 'District'],
                 ['Cadre', 'Cadre_Township', 'Township'],

                 ['Cadre', 'Cadre_University', 'University'],
                 ['Cadre', 'Cadre_Organization', 'Organization'],
                 ['Cadre', 'Cadre_Family', 'Family'],
                 ['Cadre', 'Cadre_Nation', 'Nation']
                 ]
    return kb_labels