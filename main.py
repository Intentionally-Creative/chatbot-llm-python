from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str = "gpt-4.0"
    messages: List[Message]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    try:
        # Custom system prompt
        system_prompt = {
            "role": "system",
            "content": """You are an expert in all types of alcoholic beverages, including wines, spirits, whiskeys, liqueurs, and more. 
You have deep knowledge about product types, food pairings, customer preferences, regional varieties, pricing, and regulations. 
Your job is to help customers and staff by answering liquor-related questions clearly, concisely, and accurately. 
You can help with product recommendations, explain different types of alcohol, suggest cocktail recipes, and provide advice for both casual buyers and connoisseurs.
Please follow these guidelines in your responses:
- Use simple, friendly language (as if speaking to a customer in-store).
- Keep answers concise, but don’t skip important details—be helpful.
- If a question is vague, ask clarifying questions to better assist the user.
- If the topic involves alcohol laws, provide general guidance but recommend checking local regulations.
- For food pairings or recommendations, give 1–3 good examples, not an exhaustive list."""
        }

        # Combine system message with chat history
        formatted_messages = [system_prompt] + [msg.dict() for msg in chat_request.messages]

        response = client.chat.completions.create(
            model=chat_request.model,
            messages=formatted_messages
        )

        reply = response.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        print("LLM error:", e)
        return {"reply": None, "error": str(e)}
