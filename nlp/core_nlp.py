# coding:utf-8
import os
import gensim
from nlp import model_load as nlp

model = gensim.models.Word2Vec.load("../models/word2vec/word2vec.model")


# 分词
def text_seg(sentence):
    word = list(nlp.segment(sentence))
    return word


# 词性标注
def text_pos(sentence):
    word = nlp.segment(sentence)
    pos = nlp.pos(word)
    return word, pos


# 命名实体识别
def text_ner(sentence):
    word = nlp.segment(sentence)
    pos = nlp.pos(word)
    ner = nlp.ner(word, pos)
    return word, pos, ner


def text_sentence_parse(sentence):
    """
    依存句法分析
    :param sentence:
    :return: word, pos, parser
    """
    word = nlp.segment(sentence)
    pos = nlp.pos(word)
    parsers = nlp.parse(word, pos)
    return word, pos, parsers


def word2vector(word):
    """
    近义词计算
    :param word:
    :return: topn 个相似的词
    """
    try:
        similar_words = []
        result = model.most_similar(word, topn=5)

        for word in result:
            similar_words.append(word[0])

    except:
        print('没有匹配到相似的词')

    return similar_words


def entity_nlp(entity):
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


if __name__ == '__main__':
    while True:
        line = input('please input:')
        # w = word2vector(line)
        w = text_sentence_parse(line)
        print(w)