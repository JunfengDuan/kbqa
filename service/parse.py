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

    re_label = label_filter_by_pos(words, pos)

    candidate_labels, kb_label = label_match(re_label)

    re_entity = entity_filter_by_pos(words, kb_label, pos)

    candidate_entities = entity_match(re_entity)

    topn_entities = entity_rank(candidate_entities, kb_label)


def entity_rank(candidate_entities, kb_label):
    temp_candidates = candidate_entities
    entity_str = ''.join(temp_candidates.keys())
    for word, entity_3_tuple_list in temp_candidates.items():
        for t in entity_3_tuple_list:
            score = entity_score_computer(word, t, entity_str, kb_label)
            t['score'] = score
    return temp_candidates


def entity_score_computer(word, three_tuple, entity_str, kb_label):
    entity_value = three_tuple['value']
    entity_label = three_tuple['label']
    w1 = 0.5
    w2 = 0.1
    w3 = 1 - w1
    common_count = 0
    for w in list(word):
        if w in entity_value:
            common_count += 1
    common_item = common_count / len(entity_value)
    query_item = len(entity_value) if entity_value in entity_str else 0
    label_item = 1 if entity_label in kb_label else 0
    score = w1 * common_item + w2 * query_item + w3 * label_item
    return score

def label_match(re_label):
    """
    通过实体索引库匹配实体类型
    :param re_label: 自然语言模型识别出来的label
    :return: kb_label: 通过知识库匹配提取出句子中的表示实体类型的词
    """
    label_dict = dict()
    labels = []
    kb_label = []
    for e in re_label:
        pair = {"cn_name": e}
        res = elastic.search('fayuan', 'entityDict', constraint=pair, size=4)
        if res:
            for item in res:
                if e == item['en_name']:
                    labels.append(item['en_name'])
                    kb_label.append(e)
    label_dict['word'] = kb_label
    label_dict['label'] = labels
    return label_dict, kb_label


def label_filter_by_pos(words, pos):
    """
    根据词性过滤出表示实体类型的词
    :param words:
    :param pos:
    :return:
    """
    entity_pos = ['v', 'n', 'ns', 'ni', 'nh', 'nl', 'nz', 'nt', 'nd']  # 名词和动词
    entity_object = []
    for i, p in enumerate(pos):
        if p in entity_pos:
            entity_object.append(words[i])
    return entity_object


def entity_match(entities):
    """
    通过实体索引库和近义词模型模糊匹配实体
    :param entities:
    :return:
    """
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
                res.extend(sw_res)
            entity_with_label[e] = res
    return entity_with_label


def entity_filter_by_pos(words, kb_label, pos):
    """
    根据词性过滤掉无意义的字词
    :param kb_label: 句子中表示实体类型的词
    :param words:
    :param pos:
    :return:
    """
    idle_pos = ['c', 'd', 'e,' 'g', 'h', 'nd', 'o', 'p', 'q', 'u', 'wp']
    entity_object = []
    for i, p in enumerate(pos):
        if p not in idle_pos and words[i] not in kb_label:
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
