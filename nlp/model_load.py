# coding:utf-8
import os
from pyltp import SentenceSplitter, Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller

root_dir = os.path.dirname(__file__)
LTP_DATA_DIR = os.path.join(root_dir, 'models/ltp_data_v3.4.0')  # ltp模型目录的路径

segmentor = None
postagger = None
recognizer = None
parser = None
labeller = None


# 分句
def split(text):
    sents = SentenceSplitter.split(text)
    return list(sents)


# 分词
def segment(text):
    global segmentor
    if segmentor is None:
        cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
        segmentor = Segmentor()  # 初始化实例
        segmentor.load_with_lexicon(cws_model_path, 'dict/lexicon.txt') # 加载模型，第二个参数是您的外部词典文件路径
    words = segmentor.segment(text)  # 分词
    # print(list(words))
    return words


# 词性标注
def pos(words):
    global postagger
    if postagger is None:
        pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
        postagger = Postagger() # 初始化实例
        postagger.load(pos_model_path)  # 加载模型
    postags = postagger.postag(words)
    # print(list(zip(list(words), list(postags))))
    return postags


# 实体识别
def ner(words, postags):
    global recognizer
    if recognizer is None:
        ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
        recognizer = NamedEntityRecognizer() # 初始化实例
        recognizer.load(ner_model_path)  # 加载模型
    netags = recognizer.recognize(words, postags)  # 命名实体识别
    # print(list(zip(list(words), list(postags), list(netags))))
    return netags


# 依存句法分析
def parse(words, postags):
    global parser
    if parser is None:
        par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
        parser = Parser() # 初始化实例
        parser.load(par_model_path)  # 加载模型
    arcs = parser.parse(words, postags)  # 句法分析
    # print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
    parsers = []
    for arc in arcs:
        arcl = (arc.head, arc.relation)
        parsers.append(arcl)
    return parsers


# 语义角色标注
def srl(words, postags, arcs):
    global labeller
    if labeller is None:
        srl_model_path = os.path.join(LTP_DATA_DIR, 'srl')  # 语义角色标注模型目录路径，模型目录为`srl`。注意该模型路径是一个目录，而不是一个文件。
        labeller = SementicRoleLabeller() # 初始化实例
        labeller.load(srl_model_path)  # 加载模型

    # arcs 使用依存句法分析的结果
    roles = labeller.label(words, postags, arcs)  # 语义角色标注

    # 打印结果
    role_list = []
    for role in roles:
        for arg in role.arguments:
            args = (role.index, arg.name, arg.range.start, arg.range.end)
            role_list.append(args)
    return role_list


if __name__ == '__main__':
    print('model_load')
