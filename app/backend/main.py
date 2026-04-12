from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from chatbot import ask_chatbot
from moderation import is_offensive
from tts import text_to_speech
from stt import speech_to_text
from image_gen import generate_book_image
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
def chat_endpoint(query: str):
    if is_offensive(query):
        return {"error": "Limbaj nepotrivit."}

    answer = ask_chatbot(query)
    return {"response": answer}


@app.post("/tts")
def tts_endpoint(text: str):
    audio = text_to_speech(text)
    return Response(content=audio, media_type="audio/mpeg")


@app.post("/stt")
async def stt_endpoint(file: UploadFile = File(...)):
    content = await file.read()

    with open("temp.webm", "wb") as f:
        f.write(content)

    with open("temp.webm", "rb") as f:
        text = speech_to_text(f)

    return {"text": text}


@app.post("/image")
def image_endpoint(prompt: str):
    image = generate_book_image(prompt)
    return Response(content=image, media_type="image/png")