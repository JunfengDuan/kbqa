# coding:utf-8
from nlp.core_nlp import *
from elastic.es_api import ElasticSearchClient

elastic = ElasticSearchClient('192.168.1.151', '9200')


def text_parse(text):
    """
    自然语言文本解析

    :param text: 查询语句
    :return:
    """
    words, pos, parser = text_sentence_parse(text)

    res = elastic.search('fayuan', 'propDict', )



