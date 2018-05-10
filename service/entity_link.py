from nlp.core_nlp import word2vector


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


def entity_match(entities, elastic):
    """
    通过实体索引库和近义词模型模糊匹配实体
    :param elastic:
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


def select_top_entity(topn_entities):
    """
    从候选实体中筛选分值最高的
    :param topn_entities:
    :return:
    """
    max_score_entity_dict = dict()
    for word, entity_list in topn_entities.items():
        max_score = 0
        max_score_entity = []
        for s in entity_list:
            score = s['score']
            if score > max_score:
                max_score = score
                max_score_entity.clear()
                max_score_entity.append(s)
            elif score == max_score:
                max_score_entity.append(s)
        max_score_entity_dict[word] = max_score_entity
    return max_score_entity_dict


def entity_score_computer(word, three_tuple, entity_str, kb_label):
    """
    实体打分模型
    :param word:
    :param three_tuple:
    :param entity_str:
    :param kb_label:
    :return:
    """
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
    return round(score, 2)


def entity_rank(candidate_entities, kb_label):
    """
    给候选实体排名
    :param candidate_entities:
    :param kb_label:
    :return:
    """
    temp_candidates = candidate_entities
    entity_str = ''.join(temp_candidates.keys())
    for word, entity_3_tuple_list in temp_candidates.items():
        for t in entity_3_tuple_list:
            score = entity_score_computer(word, t, entity_str, kb_label)
            t['score'] = score
    return temp_candidates
