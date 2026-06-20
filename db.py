import psycopg
import os
import dotenv
from dotenv import load_dotenv

load_dotenv() 

def get_conn():
    return psycopg.connect(conninfo=os.environ["DATABASE_URI"])

def create_conversation(conn):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO conversations DEFAULT VALUES RETURNING id, session_id, created_at;")
        row = cur.fetchone()
        return {
            "id": row[0],
            "session_id": row[1],
            "created_at": row[2]
        }

def get_conversation_id(conn, session_id):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM conversations WHERE session_id = %s", (session_id,))
        row = cur.fetchone()
        if row is None:
            raise ValueError(f"Conversation not found for session_id: {session_id}")
        return row[0]

def write_message(conn, conversation_id, role, content):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO messages (conversation_id, role, content) VALUES (%s, %s, %s) RETURNING id, role, content", (conversation_id, role, content))
        row = cur.fetchone()
        return {
            "id": row[0],
            "role": row[1],
            "content": row[2]
        }

def get_messages(conn, conversation_id):
    with conn.cursor() as cur:
        cur.execute("SELECT id, role, content FROM messages WHERE conversation_id = %s ORDER BY created_at", (conversation_id,))
        rows = cur.fetchall()
        return [{ "id": row[0], "role": row[1], "content": row[2]} for row in rows]