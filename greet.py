from fastapi import FastAPI, HTTPException
import db

app = FastAPI()

from pydantic import BaseModel

def greet(query: str) -> str:
    introduction_words = ["what", "purpose", "yourself", "do you do", "help me"]
    for word in introduction_words:
        if word in query.lower():
            return "I can answer questions like A, B, C. What can I help you with?"
    return "Hello, I am a chatbot that helps with X. I can answer questions like A, B, C."

class Prompt(BaseModel):
    prompt: str

# TODO: bring back once logic for handling 1 chat is done
# @app.get("/chats")
# def get_chats():
#     return {"chats": []}

@app.get("/chats/{session_id}/messages")
def get_chat_messages(session_id: str):
    with db.get_conn() as conn:
        try:
            conversation_id = db.get_conversation_id(conn, session_id)
        except ValueError:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        messages = db.get_messages(conn, conversation_id)
        return messages

@app.post("/chats")
def post_chat():
    with db.get_conn() as conn:
        conversation = db.create_conversation(conn)
    return {"session_id": conversation["session_id"]}

@app.post("/chats/{session_id}/messages")
def post_chat(session_id: str, prompt: Prompt):
    with db.get_conn() as conn:
        try:
            conversation_id = db.get_conversation_id(conn, session_id)
        except ValueError:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        message = db.write_message(conn, conversation_id, "user", prompt.prompt)
        return message

@app.post("/chats/{chat_id}")
def post_prompt(chat_id: int, prompt: Prompt):
    return {"chat_id": chat_id, "prompt_short": f"{prompt.prompt[:10]}...", "response": greet(prompt.prompt)}