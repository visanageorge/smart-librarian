from openai import OpenAI
import chromadb
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

chroma_client = chromadb.PersistentClient(path="data/chroma_db")
collection = chroma_client.get_collection(name="books")

query = "I want a book about friendship and adventure"

query_embedding = client.embeddings.create(
    model="text-embedding-3-small",
    input=query
).data[0].embedding

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)

for i, doc in enumerate(results["documents"][0]):
    print(f"\nResult {i+1}:")
    print(doc)
    print("Metadata:", results["metadatas"][0][i])