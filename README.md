# Smart Librarian Chatbot (RAG + Tool + Voice + Images)

## Description

This project is an AI chatbot that recommends books based on user preferences. It uses Retrieval Augmented Generation (RAG) with a vector database, combined with OpenAI models for generating responses. After recommending a book, it retrieves a detailed summary using a tool. The application also supports voice input, audio output, and optional image generation.

---

## Features

- Book recommendations based on user queries  
- Semantic search using ChromaDB and embeddings  
- Tool calling for retrieving full book summaries  
- Basic moderation for inappropriate language  
- Speech-to-text (voice input)  
- Text-to-speech (audio output with play/stop)  
- Image generation (triggered only when requested)  

---

## Architecture

Frontend (React)  
→ Backend API (FastAPI)  
→ Core logic modules:

- chatbot.py (LLM + tool calling)  
- rag.py (retrieval logic)  
- chroma_setup.py (vector database setup)  
- tools.py (book summaries)  
- moderation.py  
- tts.py  
- stt.py  
- image_gen.py  

---

## Technologies Used

### Backend
- Python  
- FastAPI  
- OpenAI API  
- ChromaDB  
- dotenv  

### Frontend
- React (Vite)  
- Fetch API  
- MediaRecorder (for voice input)  

---

## Setup

### 1. Clone the repository

```bash
git clone <repo>
cd smart-librarian
```

---

### 2. Backend setup

```bash
cd app/backend
pip install fastapi uvicorn openai chromadb python-dotenv python-multipart
```

---

### 3. Create `.env` file

```env
OPENAI_API_KEY=your_api_key_here
```

---

### 4. Initialize vector database

```bash
python chroma_setup.py
```

---

### 5. Run backend

```bash
py -m uvicorn main:app --reload
```

---

### 6. Frontend setup

```bash
cd ../frontend
npm create vite@latest . -- --template react
npm install
npm run dev
```

---

## Access

Backend:  
http://127.0.0.1:8000/docs  

Frontend:  
http://localhost:5173  

---

## Example Queries

- I want a book about friendship and adventure  
- Recommend something related to war stories  
- Generate a picture for this book  
- Tell me more about it  

---

## Application Flow

1. User sends a text or voice input  
2. If voice is used, it is converted to text  
3. The query is processed through RAG to find relevant books  
4. The LLM generates a recommendation  
5. A tool is called to retrieve the full summary  
6. Optionally, audio is generated  
7. Optionally, an image is generated  

---

## Possible Improvements

- Conversation memory (chat history)  
- Improved UI  
- Authentication  
- Streaming responses  
- Better image prompt control  
- Deployment setup  

---
