def greet(query: str) -> str:
    introduction_words = ["what", "purpose", "yourself", "do you do", "help me"]
    for word in introduction_words:
        if word in query.lower():
            return "I can answer questions like A, B, C. What can I help you with?"
    return "Hello, I am a chatbot that helps with X. I can answer questions like A, B, C."

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}