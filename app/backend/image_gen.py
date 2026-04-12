from openai import OpenAI
import os
import base64

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_book_image(prompt: str) -> bytes:
    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    return image_bytes