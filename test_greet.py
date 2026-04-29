from greet import greet
import pytest
from fastapi.testclient import TestClient
from greet import app

### Fast API tests
client = TestClient(app)

def test_get_chats():
    response = client.get("/chats")
    assert response.status_code == 200

def test_get_specific_chats():
    response = client.get("/chats/1")
    assert response.status_code == 200
    assert response.json() == {"chat_id": 1}

@pytest.mark.parametrize("input", ["What do you do?", "What's your purpose?", "Tell me about yourself", "WhAT"])
def test_prompt_known_introduction_words(input):
    response = client.post(
        "/chats/1",
        json={"prompt": input},
    )
    assert response.status_code == 200
    assert response.json() == {"chat_id": 1, "prompt_short": f"{input[:10]}...", "response": "I can answer questions like A, B, C. What can I help you with?"}

@pytest.mark.parametrize("input", ["hello", "hi", "howdy", "Tell me who you are"])
def test_prompt_unknown_introduction_words(input):
    response = client.post(
        "/chats/1",
        json={"prompt": input},
    )
    assert response.status_code == 200
    assert response.json() == {"chat_id": 1, "prompt_short": f"{input[:10]}...", "response": "Hello, I am a chatbot that helps with X. I can answer questions like A, B, C."}