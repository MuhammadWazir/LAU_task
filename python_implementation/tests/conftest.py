import pytest
from fastapi.testclient import TestClient
from main import app
from src.container import Container
from src.presentation.routers import task_router
from src.infrastructure.database.models.task import Task
from src.infrastructure.database.session import get_db


@pytest.fixture(scope="session")
def container():
    """Initialize and wire container for tests"""
    c = Container()
    c.wire(modules=[task_router])
    yield c
    c.unwire()


@pytest.fixture(scope="function", autouse=True)
def cleanup_database():
    """Clean up database before each test"""
    db = next(get_db())
    try:
        db.query(Task).delete()
        db.commit()
    finally:
        db.close()
    yield


@pytest.fixture(scope="function")
def client(container):
    """Create test client with wired container"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_task_data():
    """Sample task data for testing"""
    return {"title": "Test Task"}


@pytest.fixture
def create_sample_task(client):
    """Helper fixture to create a task"""
    def _create_task(title="Sample Task"):
        response = client.post("/tasks", json={"title": title})
        return response.json()
    return _create_task
