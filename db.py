import psycopg
import os
from dotenv import load_dotenv

load_dotenv() 

def get_conn():
    return psycopg.connect(conninfo=os.environ["DATABASE_URI"])

def create_chat(conn: psycopg.Connection):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO chats DEFAULT VALUES RETURNING id, session_id, created_at;")
        row = cur.fetchone()
        return {
            "id": row[0],
            "session_id": row[1],
            "created_at": row[2]
        }

def get_chat_id(conn: psycopg.Connection, session_id: str):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM chats WHERE session_id = %s", (session_id,))
        row = cur.fetchone()
        if row is None:
            raise ValueError(f"Chat not found for session_id: {session_id}")
        return row[0]

def write_message(conn: psycopg.Connection, chat_id: str, role: str, content: str):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO messages (chat_id, role, content) VALUES (%s, %s, %s) RETURNING id, role, content", (chat_id, role, content))
        row = cur.fetchone()
        return {
            "id": row[0],
            "role": row[1],
            "content": row[2]
        }

def get_messages(conn: psycopg.Connection, chat_id: str):
    with conn.cursor() as cur:
        cur.execute("SELECT id, role, content FROM messages WHERE chat_id = %s ORDER BY created_at", (chat_id,))
        rows = cur.fetchall()
        return [{ "id": row[0], "role": row[1], "content": row[2]} for row in rows]

def get_chats(conn: psycopg.Connection):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM chats;")
        rows = cur.fetchall()
        return [{ "id": row[0]} for row in rows]