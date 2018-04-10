# coding:utf-8
from nlp.core_nlp import *
from elastic.es_client import ElasticSearchClient
from service.util import *
elastic = ElasticSearchClient('192.168.1.151', '9200')


def text_parse(text):
    """
    自然语言文本解析

    :param text: 查询语句
    :return:
    """
    words, pos, parser = text_sentence_parse(text)

    topics = topic_word_filter(words, parser)

    entities = entity_filter_by_pos(words, pos)

    candidate_entities = entity_rank(entities)


def entity_rank(entities):

    entity_with_label = dict()
    for e in entities:
        pair = {"value": e}
        res = elastic.search('fayuan', 'propDict', constraint=pair)
        values = []
        if res:
            for item in res:
                values.append(item['value'])
            if e in values:
                entity_with_label[e] = res
                continue
        if e not in values:
            similar_words = word2vector(e)
            for sw in similar_words:
                sw_pair = {"value": sw}
                sw_res = elastic.search('fayuan', 'propDict', constraint=sw_pair)
                res.append(sw_res)
            entity_with_label[e] = res

def entity_filter_by_pos(words, pos):
    """
    根据词性过滤掉非实体的字词
    :param words:
    :param pos:
    :return:
    """
    idle_pos = ['c', 'd', 'e,' 'g', 'h', 'nd', 'o', 'p', 'q', 'u', 'wp']
    entity_object = []
    for i, p in enumerate(pos):
        if p not in idle_pos:
            entity_object.append(words[i])
    return entity_object


def topic_word_filter(words, parser):
    tags = ['HED', 'PVB', 'SBV']
    topic_word = []
    for i, p in enumerate(parser):
        tag = p[1]
        if tag in tags:
            topic_word.append(words[i])

    return topic_word
