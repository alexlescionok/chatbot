import agent

def test_formatted_prompt_includes_history():
   prompt = "What can you help me with?"
   messages = [{"id": 1, "role": "user", "content": "My name is Alex."}, {"id": 2, "role": "assistant", "content": "Hello Alex! How can I assist you today?"}]
   result = agent.format_prompt(prompt, messages)
   assert result == f"user: My name is Alex.\nassistant: Hello Alex! How can I assist you today?\nuser: {prompt}"

# TODO: add test for standalone respond function ???


def test_llm_gives_response():
    prompt = f"user: My name is Alex.\nassistant: Hello Alex! How can I assist you today?\nuser: What can you help me with?"
    result = agent.prompt_agent(prompt)
    assert result.output is not None