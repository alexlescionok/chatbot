import agent

messages = [
    {"id": "1", "role": "user", "content": "My name is Alex."},
    {"id": "2", "role": "assistant", "content": "Hello Alex! How can I assist you today?"}
]

def test_llm_gives_response():
    result = agent.prompt_agent('What can you help me with?', messages)
    assert result.output is not None