# coding:utf-8
from nlp.core_nlp import *
from service.util import *
from service.entity_link import *
from service.rel_link import *
from elastic.es_client import ElasticSearchClient
elastic = ElasticSearchClient('192.168.1.151', '9200')


def text_parse(text):
    """
    自然语言文本解析

    :param text: 查询语句
    :return:
    """
    words, pos, parser = text_sentence_parse(text)
    print('words, pos, parser:', words, pos, parser)

    topics = topic_word_filter(words, pos, parser)   # 主题词
    print('topics:', topics)

    constraint_table = collect_constraint(words, pos)  # 收集约束
    print('constraint_table:', constraint_table)

    re_label = label_filter_by_pos(words, pos)  # nlp模型识别出的label
    print('re_label:', re_label)

    candidate_labels, kb_label = label_match(re_label, elastic)  # 候选label， 句子中表示实体类型的词
    print('candidate_labels:', candidate_labels)

    re_entity = entity_filter_by_pos(words, kb_label, pos)

    candidate_entities = entity_match(re_entity, elastic)  # 候选实体/属性

    topn_entities = entity_rank(candidate_entities, kb_label)

    top_entity = select_top_entity(topn_entities)  # 待过滤的实体信息
    print('top_entity:', top_entity)

    hang_labels = label_integration(top_entity, candidate_labels)
    print('hang_labels:', hang_labels)

    rel_rdf = rel_inference(hang_labels)  # 最终的关系链
    print('rel_rdf:', rel_rdf)

    entity_list = filter_entity_by_label(top_entity, rel_rdf)  # 通过关系链中的label过滤出有用的实体和属性
    add_constraint(entity_list, constraint_table)  # 添加约束
    print('entity_list:', entity_list)

    return {'rel_rdf:': rel_rdf, 'entity_list:': entity_list}


def label_integration(top_entity, candidate_labels):
    """
    提取实体三元组中的label，整合到label集合中
    :param top_entity:
    :param candidate_labels:
    :return:
    """
    labels = candidate_labels['label']
    for v in top_entity.values():
        entity_labels = [d['label'] for d in v]
        labels.extend(entity_labels)
    return set(labels)


def topic_word_filter(words, pos, parser):
    """
    通过句法分析，提取句子中的主题词，判断返回答案
    :param pos:
    :param words:
    :param parser:
    :return:
    """
    tags = ['HED', 'PVB', 'SBV', 'ATT']
    noun = ['n', 'ni', 'nh', 'nl', 'ns', 'nz']
    topic_word = []
    for i, p in enumerate(parser):
        tag = p[1]
        if pos[i] in noun and tag == 'ATT':
            topic_word.append(words[p[0]-1])

    return topic_word


def filter_entity_by_label(top_entity, label_rdf):
    top_entity_temp = top_entity
    temp_labels = []  # ['Per', 'Loc', ...]
    for lr in label_rdf['rdf']:
        temp_labels.extend(lr)

    for e, el in top_entity_temp.items():
        for sel in el:
            label = sel['label']
            if label not in temp_labels:
                el.remove(sel)

    return top_entity_temp


def collect_constraint(words, pos):
    """
    提取查询语句中的约束
    :param words:
    :param pos:
    :return: {'汉族': '<>'}
    """
    temp_words = words
    cons = constraint_dict()
    c_table = dict()
    for i, word in enumerate(temp_words):
        if word in cons.keys() and word != words[-1]:
            c_table[words[i+1]] = cons[word]
            words.remove(word)
            pos.pop(i)
    return c_table


def add_constraint(entity_list, c_table):
    for word, info_list in entity_list.items():
        for info in info_list:
            for c_word, c_signal in c_table.items():
                if word in c_word:
                        info['op'] = c_signal
            else:
                if 'op' not in info.keys() or not info['op']:
                    info['op'] = '='
