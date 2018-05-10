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

    topics = topic_word_filter(words, parser)

    re_label = label_filter_by_pos(words, pos)

    candidate_labels, kb_label = label_match(re_label, elastic)

    re_entity = entity_filter_by_pos(words, kb_label, pos)

    candidate_entities = entity_match(re_entity, elastic)

    topn_entities = entity_rank(candidate_entities, kb_label)

    top_entity = select_top_entity(topn_entities)

    hang_labels = label_integration(top_entity, candidate_labels)

    rdf = rel_inference(hang_labels)


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


def topic_word_filter(words, parser):
    tags = ['HED', 'PVB', 'SBV']
    topic_word = []
    for i, p in enumerate(parser):
        tag = p[1]
        if tag in tags:
            topic_word.append(words[i])

    return topic_word
