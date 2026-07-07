
import db
import pytest

@pytest.fixture()
def db_conn():
    with db.get_conn() as conn:
        conn.autocommit = False
        try:
            yield conn
        finally:
            conn.rollback()

def test_create_conversation_returns_content(db_conn):
    conversation = db.create_conversation(db_conn)
    assert conversation is not None
    assert isinstance(conversation, dict)

def test_create_conversation_exists_in_db(db_conn):
    conversation_id = db.create_conversation(db_conn)["id"]
    
    with db_conn.cursor() as cur:
        cur.execute("SELECT id FROM conversations WHERE id = %s", (conversation_id,))
        row = cur.fetchone()
    
    assert row is not None
    assert row[0] == conversation_id

def test_create_conversation_unique_ids(db_conn):
    conversation_id_1 = db.create_conversation(db_conn)["id"]
    conversation_id_2 = db.create_conversation(db_conn)["id"]

    assert conversation_id_1 != conversation_id_2

def test_get_conversation_id_by_session_id(db_conn):
    conversation = db.create_conversation(db_conn)

    conversation_id = conversation["id"]
    session_id = conversation["session_id"]

    retrieved_conversation_id = db.get_conversation_id(db_conn, session_id)
    assert retrieved_conversation_id == conversation_id

def test_write_message_returns_content(db_conn):
    conversation = db.create_conversation(db_conn)
    conversation_id = conversation["id"]

    message = db.write_message(db_conn, conversation_id, "user", "hello")

    assert message is not None
    assert isinstance(message, dict)
    assert message["role"] == "user"
    assert message["content"] == "hello"

def test_get_conversation_id_raises_exception_for_nonexistent_session_id(db_conn, fake_uuid):
    with pytest.raises(ValueError):
        db.get_conversation_id(db_conn, fake_uuid)

def test_get_messages_returns_content(db_conn):
    prompts = ["hello", "hi", "howdy"]

    conversation = db.create_conversation(db_conn)
    conversation_id = conversation["id"]

    for content in prompts:
        db.write_message(db_conn, conversation_id, "user", content)

    messages = db.get_messages(db_conn, conversation_id)

    assert messages is not None
    for i, content in enumerate(prompts):
        assert messages[i]["content"] == content