from fastapi import FastAPI, HTTPException
import db
import agent

app = FastAPI()

from pydantic import BaseModel

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
        
        db.write_message(conn, conversation_id, "user", prompt.prompt)
        
        messages = db.get_messages(conn, conversation_id)

        prompt_with_history = agent.format_prompt(prompt.prompt, messages)
        
        agent_response = agent.prompt_agent(prompt_with_history)
        db.write_message(conn, conversation_id, "assistant", agent_response.output)

        return agent_response.output