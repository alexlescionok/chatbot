from fastapi import HTTPException
from app import app, responder
import agent
import db

from pydantic import BaseModel

class Prompt(BaseModel):
    prompt: str

@app.post("/chats")
def post_chat():
    with db.get_conn() as conn:
        chat = db.create_chat(conn)
    return {"session_id": chat["session_id"]}

@app.get("/chats")
def get_chats():
    with db.get_conn() as conn:
        return {"chats": db.get_chats(conn)}

@app.get("/chats/{session_id}/messages")
def get_chat_messages(session_id: str):
    with db.get_conn() as conn:
        try:
            chat_id = db.get_chat_id(conn, session_id)
        except ValueError:
            raise HTTPException(status_code=404, detail="chat not found")
        
        messages = db.get_messages(conn, chat_id)
        return {"messages": messages}

@app.post("/chats/{session_id}/messages")
def post_chat(session_id: str, prompt: Prompt):
    with db.get_conn() as conn:
        try:
            chat_id = db.get_chat_id(conn, session_id)
        except ValueError:
            raise HTTPException(status_code=404, detail="chat not found")
        
        db.write_message(conn, chat_id, "user", prompt.prompt)
        
        messages = db.get_messages(conn, chat_id)

        prompt_with_history = agent.format_prompt(prompt.prompt, messages)
        
        agent_response = agent.prompt_agent(responder, prompt_with_history)
        db.write_message(conn, chat_id, "assistant", agent_response)

        return {"response": agent_response}