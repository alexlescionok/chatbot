from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

class OllamaResponder():
    def __init__(self, model_name: str = "gemma4", base_url: str = "http://localhost:11434/v1"):
        ollama_model = OllamaModel(
            model_name, provider=OllamaProvider(base_url=base_url)
        )
        self.agent = Agent(
            ollama_model,
            instructions='Be concise, reply with one sentence.', 
        )

responder = OllamaResponder()

def format_prompt(prompt: str, messages: list[dict] = []) -> str:
    if messages:
        history = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
    else:
        history = ""
    
    prompt_with_history = f"{history}\nuser: {prompt}"
    return prompt_with_history

def prompt_agent(prompt_with_history: str) -> str:
    result = responder.agent.run_sync(prompt_with_history)
    return result

### synchronous function call
# result = prompt_agent("What is the capital of France?", messages=[])
# print(result)

# agent_hexagonal = OllamaResponder()
# print(agent_hexagonal.fake_func())

# print(agent_hexagonal.agent)

# print(agent)