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