from pydantic_ai import Agent, RunContext
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

ollama_model = OllamaModel(
    'gemma4', provider=OllamaProvider(base_url='http://localhost:11434/v1')
)
agent = Agent(
    ollama_model,
    instructions='Be concise, reply with one sentence.', 
)

def prompt_agent(prompt: str, messages: list[dict] = []) -> str:
    if messages:
        history = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
    else:
        history = ""
    full_prompt = f"{history}\nuser: {prompt}"
    result = agent.run_sync(full_prompt)
    return result

### synchronous function call
# result = prompt_agent("What is the capital of France?", messages=[])
# print(result)
