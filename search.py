# coding:utf-8
from flask import Flask, request
from cn_ner import *

app = Flask(__name__)
sxr = read_sxr('sxr.txt')
sxr_rel_dict, sxr_rel_list = read_sxr_rel('rel.txt')


@app.route('/sxr_ner', methods=['GET', 'POST'])
def sxr_ner():

    print('sxr:', sxr)
    print('sxr_rel_dict:', sxr_rel_dict)
    print('sxr_rel_list:', sxr_rel_list)

    text = request.get_json().get('text')
    print('text:', text)

    if text is None or len(text) == 0:
        return ""

    sents = get_effect_sent(text)
    sent_str = " ".join(sents)

    objects = []
    entity = text_ner(sent_str)
    sxr_objects = sx_object_extract(entity)
    if sxr_objects:
        objects.extend(sxr_objects)

    print('objects:', objects)
    obj = []
    for o in objects:
        bt = ''
        for s in sxr:
            if o in s and s in sent_str:
                if bt in s:
                    bt = s
        if len(bt) > 0 and bt not in obj:
            obj.append(bt)

    full_name = name_link(obj)
    data = str(full_name)
    return data


def name_link(ner_name):
    for i, name in enumerate(ner_name):
        for rel in sxr_rel_list:
            if name in rel:
                ner_name[i] = rel[0]
    return ner_name


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, debug=True)

