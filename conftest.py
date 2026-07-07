import pytest
import uuid
from agent import OllamaResponder
import subprocess
from dotenv import load_dotenv
import time

@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv(dotenv_path=".env.test", override=True)  # Load environment variables from .env.test file

@pytest.fixture(scope="session", autouse=True)
def get_test_conn():
    subprocess.run(["docker", "compose", "-f", "compose-test.yaml", "up", "-d"], check=True)
    time.sleep(5)
    yield
    subprocess.run(["docker", "compose", "-f", "compose-test.yaml", "down"], check=True)

@pytest.fixture()
def fake_uuid():
    return str(uuid.uuid4())

@pytest.fixture(scope="session")
def responder():
    return OllamaResponder()