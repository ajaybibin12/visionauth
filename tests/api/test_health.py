from app.core.config import settings
from tests.conftest import client


def test_health_endpoint_returns_200():
    """Health endpoint should return HTTP 200."""

    response = client.get("/api/v1/health")

    assert response.status_code == 200


def test_health_status():
    """Health endpoint should return healthy status."""

    response = client.get("/api/v1/health")

    data = response.json()

    assert data["status"] == "healthy"


def test_health_contains_application_name():
    """Application name should be returned."""

    response = client.get("/api/v1/health")

    data = response.json()

    assert data["application"] == "VisionAuth"


def test_health_contains_version():
    response = client.get("/api/v1/health")

    data = response.json()

    assert data["version"] == "0.1.0"


def test_health_contains_environment():
    response = client.get("/api/v1/health")

    data = response.json()

    assert data["environment"] == settings.environment
