# coding:utf-8

from datetime import datetime
from elasticsearch import Elasticsearch


class ElasticSearchClient(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connect()

    def connect(self):
        self.es = Elasticsearch(hosts=[{'host': self.host, 'port': self.port}])

    def count(self, index):
        """
        :param index:
        :return: 统计index总数
        """
        return self.es.count(index=index)

    def delete(self, index, doc_type, id):
        """
        :param index:
        :param doc_type:
        :param id:
        :return: 删除index中具体的一条
        """
        self.es.delete(index=index, doc_type=doc_type, id=id)

    def get(self, index, id):
        return self.es.get(index=index, id=id)

    def search(self, index, doc_type, constraint, size=20):
        try:
            doc = {"query": {"match": constraint}}
            res = self.es.search(index=index, doc_type=doc_type, body=doc, size=size)
            resources = []
            for hit in res['hits']['hits']:
                resources.append(hit["_source"])
            return resources
        except Exception as err:
            print(err)

if __name__ == '__main__':

    elastic = ElasticSearchClient('192.168.1.151', '9200')

    pairs = {"value": "北大"}
    res1 = elastic.search('fayuan', 'propDict', constraint=pairs)
    print(res1)
