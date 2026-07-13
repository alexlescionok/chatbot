
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

def test_create_chat_returns_content(db_conn):
    chat = db.create_chat(db_conn)
    assert chat is not None
    assert isinstance(chat, dict)

def test_create_chat_exists_in_db(db_conn):
    chat_id = db.create_chat(db_conn)["id"]
    
    with db_conn.cursor() as cur:
        cur.execute("SELECT id FROM chats WHERE id = %s", (chat_id,))
        row = cur.fetchone()
    
    assert row is not None
    assert row[0] == chat_id

def test_create_chat_unique_ids(db_conn):
    chat_id_1 = db.create_chat(db_conn)["id"]
    chat_id_2 = db.create_chat(db_conn)["id"]

    assert chat_id_1 != chat_id_2

def test_get_chat_id_by_session_id(db_conn):
    chat = db.create_chat(db_conn)

    chat_id = chat["id"]
    session_id = chat["session_id"]

    retrieved_chat_id = db.get_chat_id(db_conn, session_id)
    assert retrieved_chat_id == chat_id

def test_write_message_returns_content(db_conn):
    chat = db.create_chat(db_conn)
    chat_id = chat["id"]

    message = db.write_message(db_conn, chat_id, "user", "hello")

    assert message is not None
    assert isinstance(message, dict)
    assert message["role"] == "user"
    assert message["content"] == "hello"

def test_get_chat_id_raises_exception_for_nonexistent_session_id(db_conn, fake_uuid):
    with pytest.raises(ValueError):
        db.get_chat_id(db_conn, fake_uuid)

def test_get_messages_returns_content(db_conn):
    prompts = ["hello", "hi", "howdy"]

    chat = db.create_chat(db_conn)
    chat_id = chat["id"]

    for content in prompts:
        db.write_message(db_conn, chat_id, "user", content)

    messages = db.get_messages(db_conn, chat_id)

    assert messages is not None
    for i, content in enumerate(prompts):
        assert messages[i]["content"] == content


def test_get_chats_returns_no_chats(db_conn):
    
    chats = db.get_chats(db_conn)
    assert len(chats) == 0
    
def test_get_chats_returns_all_chats_that_exist(db_conn):
    
    for i in range(2):
        db.create_chat(db_conn)
    
    chats = db.get_chats(db_conn)
    assert len(chats) == 2

    for i in range(2):
        assert "id" in chats[i]
        assert isinstance(chats[i]["id"], int)