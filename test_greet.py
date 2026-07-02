from fastapi.testclient import TestClient
from greet import app

### Fast API tests
client = TestClient(app)

# TODO: bring back once logic for handling 1 chat is done
# def test_get_chats():
#     response = client.get("/chats")
#     assert response.status_code == 200

### Integration tests - to be moved to integration tests folder
def test_create_conversation():
    response = client.post(
        "/chats"
    )
    assert response.status_code == 200
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

def test_post_message_to_nonexistent_conversation_returns_404(fake_uuid):
    response = client.post(
        f"/chats/{fake_uuid}/messages",
        json={"session_id": fake_uuid, "prompt": "What do you do?"},
    )
    assert response.status_code == 404

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

