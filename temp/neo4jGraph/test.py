from neo4j import GraphDatabase
from neo4j_graphrag.retrievers import VectorRetriever
# from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.embeddings import OpenAIEmbeddings
from langchain_deepseek import ChatDeepSeek
from embedding import DashscopeOpenAIEmbeddings
# 1. Neo4j driver
URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "password")

INDEX_NAME = "index-name"

# Connect to Neo4j database
driver = GraphDatabase.driver(URI, auth=AUTH)

# 2. Retriever
# Create Embedder object, needed to convert the user question (text) to a vector
# embedder = OpenAIEmbeddings(model="text-embedding-3-large")
embedder = DashscopeOpenAIEmbeddings()
# Initialize the retriever
retriever = VectorRetriever(driver, INDEX_NAME, embedder)

# 3. LLM
# Note: the OPENAI_API_KEY must be in the env vars
# llm = OpenAILLM(model_name="gpt-4o", model_params={"temperature": 0})
llm = ChatDeepSeek(
            model="deepseek-chat",
            temperature=1.0,
            max_tokens=1024,
            timeout=None,
        )

# Initialize the RAG pipeline
rag = GraphRAG(retriever=retriever, llm=llm)

# Query the graph
query_text = "How do I do similarity search in Neo4j?"
response = rag.search(query_text=query_text, retriever_config={"top_k": 5})
print(response.answer)

from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline

kg_builder = SimpleKGPipeline(
    llm=llm, # an LLMInterface for Entity and Relation extraction
    driver=driver,  # a neo4j driver to write results to graph
    embedder=embedder,  # an Embedder for chunks
    from_pdf=False,   # set to False if parsing an already extracted text
)
# await kg_builder.run_async(file_path=str(file_path))
kg_builder.run_async(text="人工智能是计算机科学的一个分支，它包含机器学习和深度学习两个重要领域。机器学习使用统计方法来让计算机系统逐步改善性能，而深度学习则是基于神经网络的一种特殊机器学习方法。")  # if using from_pdf=False