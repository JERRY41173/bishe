"""
知识图谱类，连接到neo4j，对外呈现以下功能：
创建空的知识图谱（不支持）
删除知识图谱（不支持）

上传文件修改知识图谱
手动修改知识图谱

查询知识图谱
"""

import os
# Neo4j
from neo4j import GraphDatabase

class Database:
    """
    连接到neo4j，实现neo4j数据库级别的操作
    """
    def __init__(self):
        # 连接到neo4j,获取neo4j的所有数据库名，默认url username password已经存在环境变量中
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
        )
        # 获取neo4j的所有数据库名
        with self.driver.session() as session:
            self.databases = session.run("SHOW DATABASES").data()
        
    def get_graph_name(self):
        # 获取所有数据库名，并移除system数据库
        return [
            db['name'] for db in self.databases if db['name'] != 'system'
        ]
    
    def change_current_graph(self, graph_name):
        # 传入数据库名，核验后更改Neo4jGraph对象的数据库名
        
        if graph_name in self.get_graph_name():
            #返回成功信息，供调用者判断
            return f"Graph changed to {graph_name}."
        else:
            return "Graph name not found in databases."
        
    def create_graph(self, graph_name):
        #创建一个新的知识图谱
        try:
            with self.driver.session() as session:
                session.run(f"CREATE DATABASE {graph_name}")
            # 切换到新创建的数据库
            self.change_graph(graph_name)
            return f"Graph {graph_name} created successfully."
        except Exception as e:
        # 社区版不支持多数据库，直接返回报错信息
            return "Neo4j Community Edition does not support multiple databases. Please use the default database."

    def delete_graph(self,graph_name):
        try:
            # 删除一个知识图谱
            with self.driver.session() as session:
                session.run(f"DROP DATABASE {graph_name}")
            # 切换到默认数据库
            self.change_graph(self.get_graph_name()[0])
            return f"Graph {graph_name} deleted successfully."
        except Exception as e:
        # 社区版不支持多数据库，直接返回报错信息
            return "Neo4j Community Edition does not support multiple databases. Please use the default database."

class Graph:
    """
    连接到neo4j特定数据库，实现对知识图谱的操作
    获取该数据库的完整图谱
    上传文件修改知识图谱（暂时不做）
    增加节点/关系
    删除节点/关系
    修改节点/关系
    """
    # 如果传入了Database对象，则使用该对象
    def __init__(self, graph_name:str, graph_databas:Database=None):
        # 如果传入了GraphDatabase对象，则使用该对象
        # 否则创建一个新的GraphDatabase对象
        if graph_databas:
            self.database = graph_databas
        else:
            self.database = Database()
        # 如果传入了数据库名，则使用该数据库名
        # 否则使用默认数据库
        if graph_name not in self.database.get_graph_name():
            raise ValueError(f"Graph name {graph_name} not found in databases.")
        self.graph_name = graph_name
        self.driver = self.database.driver
    def get_graph(self):
        # 获取该数据库的完整图谱,返回node列表和relationship列表
        try:
            with self.driver.session() as session:
                nodesResult = session.run("MATCH (n) RETURN n")
                relationshipsResult = session.run("MATCH ()-[r]->() RETURN r")
                return [record['n'] for record in nodesResult], [record['r'] for record in relationshipsResult]
        except Exception as e:
            return f"Error retrieving graph: {e}"

    def add_node(self, node):
        # 增加节点
        try:
            with self.driver.session() as session:
                session.run("CREATE (n:Node {name: $name})", name=node)
        except Exception as e:
            return f"Error adding node: {e}"

    def add_relationship(self, start_node, end_node, relationship):
        # 增加关系
        try:
            with self.driver.session() as session:
                session.run(
                    "MATCH (a:Node {name: $start_node}), (b:Node {name: $end_node}) "
                    "CREATE (a)-[r:RELATIONSHIP {type: $relationship}]->(b)",
                    start_node=start_node,
                    end_node=end_node,
                    relationship=relationship
                )
        except Exception as e:
            return f"Error adding relationship: {e}"

    def delete_node(self, node):
        # 删除节点
        try:
            with self.driver.session() as session:
                session.run("MATCH (n:Node {name: $name}) DELETE n", name=node)
        except Exception as e:
            return f"Error deleting node: {e}"

    def delete_relationship(self, start_node, end_node, relationship):
        # 删除关系
        try:
            with self.driver.session() as session:
                session.run(
                    "MATCH (a:Node {name: $start_node})-[r:RELATIONSHIP {type: $relationship}]->(b:Node {name: $end_node}) "
                    "DELETE r",
                    start_node=start_node,
                    end_node=end_node,
                    relationship=relationship
                )
        except Exception as e:
            return f"Error deleting relationship: {e}"

    def update_node(self, old_node, new_node):
        # 修改节点
        try:
            with self.driver.session() as session:
                session.run(
                    "MATCH (n:Node {name: $old_node}) "
                    "SET n.name = $new_node",
                    old_node=old_node,
                    new_node=new_node
                )
        except Exception as e:
            return f"Error updating node: {e}"

    def update_relationship(self, start_node, end_node, old_relationship, new_relationship):
        # 修改关系
        try:
            with self.driver.session() as session:
                session.run(
                    "MATCH (a:Node {name: $start_node})-[r:RELATIONSHIP {type: $old_relationship}]->(b:Node {name: $end_node}) "
                    "SET r.type = $new_relationship",
                    start_node=start_node,
                    end_node=end_node,
                    old_relationship=old_relationship,
                    new_relationship=new_relationship
                )
        except Exception as e:
            return f"Error updating relationship: {e}"
    
#  单元测试
if __name__ == "__main__":
    # 验证环境变量
    print("NEO4J_URI:", os.getenv("NEO4J_URI"))
    print("NEO4J_USERNAME:", os.getenv("NEO4J_USERNAME"))
    print("NEO4J_PASSWORD:", os.getenv("NEO4J_PASSWORD"))

    #创建Database对象验证neo4j连接
    thisDatabase = Database()
    # 获取所有数据库名
    print("All databases:", thisDatabase.get_graph_name())
    # 创建一个新的知识图谱
    print(thisDatabase.create_graph("test_graph"))
    # 删除一个知识图谱
    print(thisDatabase.delete_graph("test_graph"))
    
    #创建Graph对象测试图谱编辑
    thisgraph = Graph("neo4j", thisDatabase)
    nodes,relationships = thisgraph.get_graph()
    print([node['name'] for node in nodes],[relationship.start_node for relationship in relationships])
    def print_graph(graph):
        # 打印图谱
        nodes, relationships = graph.get_graph()
        print("Nodes:", [node['name'] for node in nodes])
        # 根据relationships的nodes属性获取关系的起始节点和结束节点
        relationships = [
            {
                'start_node': relationship.start_node['name'],  
                'end_node': relationship.end_node['name'],
                'type': relationship['type']
            }
            for relationship in relationships
        ]
        # 打印关系
        print("Relationships:",relationships)
    # 获取该数据库的完整图谱
    print_graph(thisgraph)
    # # 增加节点
    # thisgraph.add_node("test_node")
    # thisgraph.add_node("test_node2")
    # # 增加关系
    # thisgraph.add_relationship("test_node", "test_node2", "test_relationship")
    print_graph(thisgraph)
    # # # 删除节点
    # thisgraph.delete_node("test_node")
    # # 删除关系
    # thisgraph.delete_relationship("test_node", "test_node2", "test_relationship")
    # thisgraph.delete_node("test_node")
    # thisgraph.delete_node("test_node2")
    # print_graph(thisgraph)
    
    
    