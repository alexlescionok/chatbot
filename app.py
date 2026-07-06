from fastapi import FastAPI
from agent import OllamaResponder

app = FastAPI()
responder = OllamaResponder()