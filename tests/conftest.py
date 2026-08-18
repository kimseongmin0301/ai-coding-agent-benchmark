import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.store import reset_users


@pytest.fixture(autouse=True)
def reset_store():
    reset_users()
    yield
    reset_users()


@pytest.fixture
def client():
    return TestClient(app)
