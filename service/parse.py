# coding:utf-8
import os

from nlp import core_nlp as nlp


def text_parse(text):
    """
    自然语言文本解析

    :param text: 查询语句
    :return:
    """
    words = text_ner(text)


# 读文件
def read_file(path):
    with open(path, 'rt', encoding='utf-8') as f:
        data = f.read()
    return data


# 加载受信人列表
def read_sxr(sxr_file):
    sxr_file_path = os.path.join('dict', sxr_file)
    person = []
    with open(sxr_file_path, 'r') as f:
        for line in f.readlines():
            line = line.replace('\n', '').replace(' ', '')
            person.append(line)
    return person


# 加载受信人关联关系列表
def read_sxr_rel(sxr_file):
    sxr_file_path = os.path.join('dict', sxr_file)
    person_rel_dict = dict()
    person_rel_list = []
    with open(sxr_file_path, 'r') as f:
        for line in f.readlines():
            line = line.replace('\n', '')
            name_short = line.split(':')
            person_rel_dict[name_short[0]] = name_short[1].split(' ')
            full_name = [name_short[0]]
            full_name.extend(name_short[1].split(' '))
            person_rel_list.append(full_name)
    return person_rel_dict, person_rel_list


def text_ner(sentence):
    """
    实体识别
    sentence='毕业于北京大学的干部'

    :param sentence:
    :return:
    """
    word = nlp.segment(sentence)
    pos = nlp.pos(word)
    ner = nlp.ner(word, pos)
    entity = list(zip(list(word), list(pos), list(ner)))
    return entity


def entity_extract(entity):
    """
    实体抽取
    entity=[('尊敬', 'v', 'O'), ('的', 'u', 'O'), ('习大大', 'nh', 'S-Nh'), ('您好', 'i', 'O')]

    :param entity:
    :return:
    """
    label = ['S-Nh', 'S-Ni']
    pos = ['n', 'ni', 'nh,' 'ns', 'nl']
    entity_object = []
    for n in entity:
        if n[2] in label or n[1] in pos:
            entity_object.append(n[0])
    return entity_object


# 得到包含受信对象的语句
def get_effect_sent(text):
    sentences = nlp.split(text)
    # print('\n'.join(sentences))

    effective_sents = [sentences[0], sentences[sentences.__len__() - 1]]
    return effective_sents


if __name__ == '__main__':

    file_path = '/home/jfd/Documents/信访/数据/史主任发来103个案例(20180223)/2017022857760.txt'
    doc = read_file(file_path)
    sents = get_effect_sent(doc)
    text_sx = []
    for t in sents:
        entities = text_ner(t)
        sx_objects = sx_object_extract(entities)
        sent_object = (t, sx_objects)
        text_sx.append(sent_object)
    for x in text_sx:
        print(x)



