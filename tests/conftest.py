from fastapi.testclient import TestClient

from app.main import app


def get_test_client() -> TestClient:
    """Create FastAPI test client."""

    return TestClient(app)


client = get_test_client()
