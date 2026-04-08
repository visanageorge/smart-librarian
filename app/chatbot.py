from openai import OpenAI
from dotenv import load_dotenv
import os
import json

from rag import retrieve_books
from tools import get_summary_by_title

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_chatbot(query):
    # Dam retrieve celor mai relevante carti cu retrieve_books
    documents, titles = retrieve_books(query)
    context = "\n\n".join(documents)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful librarian. Recommend ONE book from the provided context and use the tool to provide its full summary."},
            {"role": "system", "content": f"Relevant books:\n{context}"},
            {"role": "system", "content": f"Available titles: {', '.join(titles)}"},
            {"role": "system", "content": "When calling the tool, you MUST use exactly one of the provided titles. Do not invent or modify titles."},
            {"role": "user", "content": query}
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "get_summary_by_title",
                    "description": "Get a summary of a book by its title.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The title of the book."
                            }
                        },
                        "required": ["title"]
                    }
                }
            }
        ],
        tool_choice="auto"
    )

    message = response.choices[0].message

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        
        tool_args = json.loads(tool_call.function.arguments)
        title = tool_args["title"]

        summary = get_summary_by_title(title)

        final_response = client.chat.completions.create(
            model="gpt-4o-mini",    
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides information about books."},
                {"role": "system","content": f"Available titles: {', '.join(titles)}"},
                {"role": "user", "content": f"Based on the following context, answer the question: {query}\n\nContext:\n{context}"},
                {"role": "assistant", "content": message.content or "",
                    "tool_calls": [
                                {
                                    "id": tool_call.id,
                                    "type": "function",
                                    "function": {
                                        "name": tool_call.function.name,
                                        "arguments": tool_call.function.arguments
                                    }
                                }
                    ]
                    },
                {"role": "tool", "tool_call_id": tool_call.id, "content": summary}
            ]
        )
        return final_response.choices[0].message.content
    
    return message.content

def chat():
    print("📚 Smart Librarian Chatbot (type 'exit' to quit)\n")

    while True:
        query = input("You: ")

        if query.lower() == "exit":
            break

        answer = ask_chatbot(query)
        print("\nBot:", answer, "\n")


if __name__ == "__main__":
    chat()