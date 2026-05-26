
import psycopg

import db

### DB tests
def test_create_conversation_returns_id():
    conversation = db.create_conversation()
    assert conversation is not None
    assert isinstance(conversation, dict)

def test_create_conversation_exists_in_db():
    conversation_id = db.create_conversation()["id"]
    
    with psycopg.connect(conninfo="postgresql://chatbot_user:localpassword@0.0.0.0:5432/chatbot") as conn:

        # Open a cursor to perform database operations
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM conversations WHERE id = %s", (conversation_id,))
            row = cur.fetchone()
    
    assert row is not None
    assert row[0] == conversation_id

def test_create_conversation_unique_ids():
    conversation_id_1 = db.create_conversation()["id"]
    conversation_id_2 = db.create_conversation()["id"]

    assert conversation_id_1 != conversation_id_2