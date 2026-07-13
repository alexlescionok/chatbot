from pyexpat.errors import messages

from fastapi.testclient import TestClient
from app import app
import routes

### Fast API tests
client = TestClient(app)

def test_get_chats_returns_empty_list_when_no_chats_exist():
    response = client.get("/chats")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_chats_returns_list_of_existing_chats():
    # 1st conversation
    response = client.post(
        "/chats"
    )
    session_id = response.json()["session_id"]

    response = client.post(
        f"/chats/{session_id}/messages",
        json={"session_id": session_id, "prompt": "What do you do?"},
    )

    # 2nd conversation
    response = client.post(
        "/chats"
    )
    session_id = response.json()["session_id"]

    response = client.post(
        f"/chats/{session_id}/messages",
        json={"session_id": session_id, "prompt": "Tell me about chatbots"},
    )
    
    response = client.get("/chats")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    for conversation in response.json():
        assert "id" in conversation

def test_create_conversation():
    response = client.post(
        "/chats"
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "session_id" in response.json()

def test_post_message_to_conversation():
    response = client.post(
        "/chats"
    )
    session_id = response.json()["session_id"]

    response = client.post(
        f"/chats/{session_id}/messages",
        json={"session_id": session_id, "prompt": "What do you do?"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "response" in response.json()

def test_post_message_to_nonexistent_conversation_returns_404(fake_uuid):
    response = client.post(
        f"/chats/{fake_uuid}/messages",
        json={"session_id": fake_uuid, "prompt": "What do you do?"},
    )
    assert response.status_code == 404
    assert isinstance(response.json(), dict)
    assert "detail" in response.json()

def test_get_message_in_conversation():
    response = client.post(
        "/chats"
    )
    session_id = response.json()["session_id"]

    response = client.post(
        f"/chats/{session_id}/messages",
        json={"session_id": session_id, "prompt": "What do you do?"},
    )

    response = client.get(
        f"/chats/{session_id}/messages"
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for message in response.json():
        assert "id" in message
        assert "role" in message
        assert "content" in message