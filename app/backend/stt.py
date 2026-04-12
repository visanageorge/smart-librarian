from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def speech_to_text(file):
    transcript = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=file
    )

    return transcript.text