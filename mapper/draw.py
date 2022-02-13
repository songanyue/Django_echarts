import csv
from py2neo import Graph, Node, Relationship, NodeMatcher

g = Graph(host="localhost", user="neo4j", password="say0523")
g.run('match (n) detach delete n')

with open("neo4j.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for item in reader:
        if reader.line_num == 1:
            continue
        print("当前行数：", reader.line_num, "当前内容：", item)

        start_node = Node("Good", name=item[0])
        g.merge(start_node, "Good", "name")
        end_node = Node("Country", name=item[1])
        g.merge(end_node, "Country", "name")
        relation = Relationship(start_node, item[2], end_node)
        g.merge(relation, "Trade", "name")

country_list = ['澳大利亚', '巴西', '法国', '德国', '日本', '韩国', '印度', '意大利', '荷兰', '美国', '英国', '俄罗斯']
for i in country_list:
    start_node = Node("Country", name=i)
    end_node = Node("Country", name='中国')
    relation = Relationship(start_node, item[2], end_node)
    g.merge(relation, "Trade", "name")