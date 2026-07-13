import agent

def test_formatted_prompt_includes_history():
   prompt = "What can you help me with?"
   messages = [{"id": 1, "role": "user", "content": "My name is Alex."}, {"id": 2, "role": "assistant", "content": "Hello Alex! How can I assist you today?"}]
   result = agent.format_prompt(prompt, messages)
   assert result == f"user: My name is Alex.\nassistant: Hello Alex! How can I assist you today?\nuser: {prompt}"

def test_agent_gives_response(responder):
    prompt = f"user: My name is Alex.\nassistant: Hello Alex! How can I assist you today?\nuser: What can you help me with?"
    result = agent.prompt_agent(responder, prompt)
    assert result is not None