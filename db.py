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
        return row[0] if row else None

def write_message(conn, conversation_id, role, content):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO messages (conversation_id, role, content) VALUES (%s, %s, %s) RETURNING id, content", (conversation_id, role, content))
        row = cur.fetchone()
        return {
            "id": row[0],
            "content": row[1]
        }