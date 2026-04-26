from greet import greet
import pytest

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