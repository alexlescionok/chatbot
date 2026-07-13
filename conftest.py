import pytest
import uuid
from agent import OllamaResponder
import subprocess
from dotenv import load_dotenv
import time
import db

@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv(dotenv_path=".env.test", override=True)  # Load environment variables from .env.test file

@pytest.fixture(scope="session", autouse=True)
def get_test_conn(load_env): # Pass load_env explicitly to ensure it runs before this fixture
    subprocess.run(["docker", "compose", "-f", "compose-test.yaml", "up", "-d"], check=True)
    time.sleep(5)
    yield
    subprocess.run(["docker", "compose", "-f", "compose-test.yaml", "down"], check=True)

@pytest.fixture(scope="session", autouse=True)
def clean_db_session(get_test_conn): # Pass get_test_conn explicitly to ensure it runs before this fixture
    with db.get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE messages, conversations RESTART IDENTITY CASCADE;")
        conn.commit()
    

@pytest.fixture()
def fake_uuid():
    return str(uuid.uuid4())

@pytest.fixture(scope="session")
def responder():
    return OllamaResponder()