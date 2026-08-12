from fastapi.testclient import TestClient


def test_create_user(client: TestClient):
    # Test creating a new user
    payload = {
        "employee_id": "EMP001",
        "email": "john@example.com",
        "full_name": "John Doe",
    }

    response = client.post("/api/v1/users", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["user"]["employee_id"] == payload["employee_id"]
    assert data["user"]["email"] == payload["email"]
    assert data["user"]["full_name"] == payload["full_name"]
    assert data["user"]["is_active"] is True

    assert "id" in data["user"]
    assert "created_at" in data["user"]
    assert "updated_at" in data["user"]


def test_create_user_duplicate_email(client: TestClient):
    """Creating a user with an existing email should return HTTP 409."""

    first = {
        "employee_id": "EMP001",
        "email": "john@example.com",
        "full_name": "John Doe",
    }

    second = {
        "employee_id": "EMP002",
        "email": "john@example.com",
        "full_name": "Jane Doe",
    }

    client.post("/api/v1/users", json=first)

    response = client.post("/api/v1/users", json=second)

    assert response.status_code == 409


def test_create_user_duplicate_employee_id(client: TestClient):
    """Creating a user with an existing employee ID should return HTTP 409."""

    first = {
        "employee_id": "EMP001",
        "email": "john@example.com",
        "full_name": "John Doe",
    }

    second = {
        "employee_id": "EMP001",
        "email": "jane@example.com",
        "full_name": "Jane Doe",
    }

    client.post("/api/v1/users", json=first)

    response = client.post("/api/v1/users", json=second)

    assert response.status_code == 409
