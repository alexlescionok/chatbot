def greet(query: str) -> str:
    introduction_words = ["what", "purpose", "yourself", "do you do", "help me"]
    for word in introduction_words:
        if word in query.lower():
            return "I can answer questions like A, B, C. What can I help you with?"
    return "Hello, I am a chatbot that helps with X. I can answer questions like A, B, C."

from fastapi import FastAPI

app = FastAPI()

from pydantic import BaseModel

class Prompt(BaseModel):
    prompt: str

@app.get("/chats")
def get_chats():
    return {"chats": []}


@app.get("/chats/{chat_id}")
def get_chats(chat_id: int):
    return {"chat_id": chat_id}

@app.post("/chats/{chat_id}")
def post_prompt(chat_id: int, item: Prompt):
    return {"chat_id": chat_id, "prompt_short": f"{item.prompt[:10]}..."}