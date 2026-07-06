import pytest
import uuid
from agent import OllamaResponder

@pytest.fixture()
def fake_uuid():
    return str(uuid.uuid4())

@pytest.fixture()
def responder():
    return OllamaResponder()