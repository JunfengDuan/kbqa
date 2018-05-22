import service.util as util


def label_match(re_label, elastic):
    """
    通过实体索引库匹配实体类型
    :param elastic:
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
                if e == item['cn_name']:
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
    entity_object = [words[i] for i, p in enumerate(pos) if p in entity_pos]
    return entity_object


def rel_inference(hang_labels):
    """
    关系推理，根据知识库提供的N元组路径筛选实体类型
    :param hang_labels: 候选实体类型
    :return: {score:1, rdf:[[n元关系链], [], ...]}
    """
    rdf_dict = dict()
    if not hang_labels:
        return rdf_dict
    if len(hang_labels) <= 1:
        rdf_dict = {'score': 'max', 'rdf': [hang_labels]}
        return rdf_dict

    kb_labels = util.get_kblabels()
    score_rdf = [rel_score_computer(hang_labels, kb_label) for kb_label in kb_labels]
    max_score = 0.01
    max_score_rdf = []
    for item in score_rdf:
        score = item['score']
        rdf = item['rdf']
        if score > max_score:
            max_score = score
            max_score_rdf.clear()
            max_score_rdf.append(rdf)
        elif score == max_score:
            max_score_rdf.append(rdf)
        rdf_dict = {'score': max_score, 'rdf': max_score_rdf}
    return rdf_dict


def rel_score_computer(hang_labels, kb_label):
    """
    关系打分模型
    :param hang_labels:
    :param kb_label:['Person', 'Birth_Place', 'Address']
    :return:
    """
    score = 0
    for l in hang_labels:
        if l in kb_label:
            score += 1

    if score == len(hang_labels):
        score += len(hang_labels)

    if score == 1:
        score = 0

    score = score / len(kb_label)
    return {'score': round(score, 2), 'rdf': kb_label}