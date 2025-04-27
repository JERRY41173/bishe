import os
from neo4j_graphrag.embeddings import Embedder
from openai import OpenAI

# Initialize the DashScope client
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # Alternatively, replace with your API key string
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

class CustomEmbeddings(Embedder):
    def __init__(self, client = None, model="text-embedding-v3", dimensions=1024, encoding_format="float"):
        self.client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),  # Alternatively, replace with your API key string
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        self.model = model
        self.dimensions = dimensions
        self.encoding_format = encoding_format

    def embed_query(self, text: str) -> list[float]:
        # Call the DashScope service to generate embeddings.
        # The call below assumes the client's embeddings method returns a dict with key "embedding".
        response = self.client.embeddings.create(input=text, model=self.model,dimensions=self.dimensions)
        return response.data[0].embedding

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_query(text) for text in texts]


# llm = CustomEmbeddings(client=client)
# res = llm.embed_query("text")
# print(res[:10])