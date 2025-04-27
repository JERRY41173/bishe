from neo4j import GraphDatabase
from neo4j_graphrag.indexes import create_vector_index

NEO4J_URI = "neo4j://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "password"
INDEX_NAME = "vector-index-name"

# Connect to the Neo4j database
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

# Create the index
create_vector_index(
    driver,
    INDEX_NAME,
    label="Chunk",
    embedding_property="embedding",
    dimensions=1024,
    similarity_fn="euclidean",
)


print("Index created successfully.")

def delete_index(driver, index_name):
    with driver.session() as session:
        # Drop the index using Cypher's DROP INDEX command; the index name is wrapped in backticks.
        session.run(
            f"DROP INDEX `{index_name}` IF EXISTS"
        )
    print(f"Index {index_name} deleted successfully.")

# 删除索引
# delete_index(driver, INDEX_NAME)

driver.close()
