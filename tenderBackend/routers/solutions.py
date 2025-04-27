from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

#引用manager文件夹下 的graph.py文件
from manager.graph import Graph

router = APIRouter(
    prefix="/solutions",
    tags=["solutions"],
    responses={404: {"description": "Not found"}},
)

thisgraph = Graph("neo4j")

@router.get("/graph")
async def getGraph():
    """
    使用Graph获取图谱
    """
    nodes, relationships = thisgraph.get_graph()
    nodes = [node['name'] for node in nodes]
    relationships=[
            {
                'start_node': relationship.start_node['name'],
                'end_node': relationship.end_node['name'],
                'type': relationship['type']
            }
            for relationship in relationships
        ]
    print("Nodes:", nodes)
    print("Relationships:", relationships)
    return {
        "nodes": nodes,
        "relationships": relationships
    }