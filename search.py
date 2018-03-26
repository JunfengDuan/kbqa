# coding:utf-8
from flask import Flask, request

from service.parse import *

app = Flask(__name__)


@app.route('/search', methods=['GET', 'POST'])
def search():
    """
    问答搜索
    :return:
    """
    data = ""

    text = request.get_json().get('text')
    print('text:', text)

    if text is None or len(text) == 0:
        return ""

    result = text_parse(text)
    data = str(result)

    return data


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, debug=True)

