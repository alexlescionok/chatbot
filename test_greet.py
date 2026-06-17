import pytest
import uuid
from fastapi.testclient import TestClient
from greet import app

### Fast API tests
client = TestClient(app)

# TODO: bring back once logic for handling 1 chat is done
# def test_get_chats():
#     response = client.get("/chats")
#     assert response.status_code == 200

# TODO: re-write this to use session_id instead of chat_id§
# def test_get_specific_chats():
#     response = client.get("/chats/1")
#     assert response.status_code == 200
#     assert response.json() == {"chat_id": 1}


@pytest.mark.parametrize("input", ["hello", "hi", "howdy", "Tell me who you are"])
def test_prompt_unknown_introduction_words(input):
    response = client.post(
        "/chats/1",
        json={"prompt": input},
    )
    assert response.status_code == 200
    assert response.json() == {"chat_id": 1, "prompt_short": f"{input[:10]}...", "response": "Hello, I am a chatbot that helps with X. I can answer questions like A, B, C."}

### Integration tests - to be moved to integration tests folder
def test_create_conversation():
    response = client.post(
        "/chats"
    )
    assert response.status_code == 200
    assert "session_id" in response.json()

@pytest.mark.parametrize("input", ["What do you do?", "What's your purpose?", "Tell me about yourself", "WhAT"])
def test_post_message_to_conversation(input):
    response = client.post(
        "/chats"
    )
    session_id = response.json()["session_id"]

    response = client.post(
        f"/chats/{session_id}/messages",
        json={"session_id": session_id, "prompt": input},
    )
    assert response.status_code == 200

def test_post_message_to_nonexistent_conversation_returns_404():
    fake_uuid = str(uuid.uuid4())
    response = client.post(
        f"/chats/{fake_uuid}/messages",
        json={"session_id": fake_uuid, "prompt": "What do you do?"},
    )
    assert response.status_code == 404