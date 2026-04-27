from greet import greet
import pytest
from fastapi.testclient import TestClient
from greet import app

'''
Test greeting 
1. Write a test where a user input of “hello” results in chatbot responding with what the purpose of the chat bot is (its introduction)
2. Write a test where “hi” does the same as above
3. Write a test where howdy does the same as above
'''

@pytest.mark.parametrize("input", ["hello", "hi", "howdy"])
def test_greeting(input):
    result = greet(input)
    assert result == "Hello, I am a chatbot that helps with X. I can answer questions like A, B, C."

@pytest.mark.parametrize("input", ["What do you do?", "What's your purpose?", "Tell me about yourself", "WhAT"])
def test_ask_info(input):
    result = greet(input)
    assert result == "I can answer questions like A, B, C. What can I help you with?"

### Fast API tests
client = TestClient(app)

def test_get_chats():
    response = client.get("/chats")
    assert response.status_code == 200

def test_get_specific_chats():
    response = client.get("/chats/1")
    assert response.status_code == 200
    assert response.json() == {"chat_id": 1}

def test_prompt_known_introduction_words():
    response = client.post(
        "/chats/1",
        json={"prompt": "Tell me what you do"},
    )
    assert response.status_code == 200
    assert response.json() == {"chat_id": 1, "prompt_short": "Tell me wh...", "response": "I can answer questions like A, B, C. What can I help you with?"}

def test_prompt_unknown_introduction_words():
    response = client.post(
        "/chats/1",
        json={"prompt": "Tell me who you are"},
    )
    assert response.status_code == 200
    assert response.json() == {"chat_id": 1, "prompt_short": "Tell me wh...", "response": "Hello, I am a chatbot that helps with X. I can answer questions like A, B, C."}