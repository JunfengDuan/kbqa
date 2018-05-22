# coding:utf-8

from py2neo import Graph, NodeSelector
from pandas import DataFrame


class Neo4jClient(object):

    def __init__(self, user='neo4j', password='neo4j', host='localhost', port=7687):
        # self.db = Database("bolt://camelot.example.com:7687")
        self.graph = Graph(bolt=True, host=host, bolt_port=port, user=user, password=password)
        self.selector = NodeSelector(self.graph)

    def get_graph(self, cypher):
        data = self.graph.data(cypher)
        return list(data)

    def get_data_frame(self, cypher):
        data = self.graph.data(cypher)
        return DataFrame(data)

    def select(self, labels, props):
        data = self.selector.select(labels, props)
        return list(data)

    def select_where(self, label, constraint):
        selected = self.selector.select(label).where(constraint)
        return list(selected)

    def cypher_execute(self, cypher):
        result = self.graph.cypher.execute(cypher)
        return result


if __name__ == '__main__':

    cy = 'MATCH (cadre:Cadre)-[cadre_city:Cadre_City]->(city:City) RETURN cadre,cadre_city,city LIMIT 2'
    # cy1 = 'MATCH p = (cadre:Cadre)-[cadre_city:Cadre_City]->(city:City) RETURN p LIMIT 2'

    neo4j_client = Neo4jClient('neo4j', 'Neo4j', '192.168.1.151', 7600)
    # neo4j_client = Neo4jClient('neo4j', 'Neo4j')

    # d1 = neo4j_client.get_graph(cy)
    # d1 = neo4j_client.get_data_frame(cy)
    d1 = neo4j_client.select(('Cadre',), {'name': '人员1475'})
    # d1 = neo4j_client.select_where('Cadre', "_.name='人员1475'")
    # d1 = neo4j_client.select_where('Cadre', "_.nation='汉族' and _.gender='女'")

    for item in d1:
        print(item)




