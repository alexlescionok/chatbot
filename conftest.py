import pytest
import uuid

@pytest.fixture()
def fake_uuid():
    return str(uuid.uuid4())