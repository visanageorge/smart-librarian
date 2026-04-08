from dotenv import load_dotenv
import os
import chromadb
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# Citim fisierul
with open("data/book_summaries.md", "r", encoding="utf-8") as f:
    text = f.read()

# Spargem pe carti
books = text.split("## Title:")
books = [b.strip() for b in books if b.strip()]

documents = []
metadatas = []
ids = []

for i, book in enumerate(books):
    lines = book.split("\n", 1)

    if len(lines) < 2:
        continue

    title = lines[0].strip()
    summary = lines[1].strip()

    full_text = f"Title: {title}\nSummary: {summary}"

    documents.append(full_text)
    metadatas.append({"title": title})
    ids.append(title.lower().replace(" ", "_").replace("'", "").replace("’", ""))

# Cream embeddings
embeddings = []
for doc in documents:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=doc
    )
    embeddings.append(response.data[0].embedding)

# Initializam ChromaDB
chroma_client = chromadb.PersistentClient(path="data/chroma_db")
collection = chroma_client.get_or_create_collection(name="books")

# Salvam in DB
collection.add(
    documents=documents,
    metadatas=metadatas,
    embeddings=embeddings,
    ids=ids
)

print("Data loaded into ChromaDB!")