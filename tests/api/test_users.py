from uuid import uuid4

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


def test_get_user(client: TestClient, user):
    response = client.get(f"/api/v1/users/{user.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["user"]["id"] == str(user.id)
    assert data["user"]["email"] == user.email
    assert data["user"]["employee_id"] == user.employee_id
    assert data["user"]["full_name"] == user.full_name
    assert data["user"]["is_active"] is True


def test_get_user_not_found(client: TestClient):
    """GET /users/{user_id} should return 404 for a missing user."""

    user_id = uuid4()

    response = client.get(f"/api/v1/users/{user_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"User with ID {user_id} not found."


def test_list_users(client):
    """GET /users should return all users."""

    client.post(
        "/api/v1/users/",
        json={
            "employee_id": "EMP-001",
            "email": "john@example.com",
            "full_name": "John Doe",
        },
    )

    client.post(
        "/api/v1/users/",
        json={
            "employee_id": "EMP-002",
            "email": "jane@example.com",
            "full_name": "Jane Doe",
        },
    )

    response = client.get("/api/v1/users/")

    assert response.status_code == 200

    data = response.json()

    assert "users" in data
    assert len(data["users"]) == 2

    assert data["users"][0]["employee_id"] == "EMP-001"
    assert data["users"][1]["employee_id"] == "EMP-002"


def test_list_users_empty(client):
    """GET /users should return an empty list when no users exist."""

    response = client.get("/api/v1/users/")

    assert response.status_code == 200

    data = response.json()

    assert data["users"] == []


def test_update_user(client):
    """API should update an existing user."""

    create_response = client.post(
        "/api/v1/users/",
        json={
            "employee_id": "EMP-001",
            "email": "john@example.com",
            "full_name": "John Doe",
        },
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["user"]["id"]

    response = client.patch(
        f"/api/v1/users/{user_id}",
        json={
            "full_name": "John Updated",
            "email": "john.updated@example.com",
        },
    )

    assert response.status_code == 200

    data = response.json()["user"]

    assert data["id"] == user_id
    assert data["employee_id"] == "EMP-001"
    assert data["email"] == "john.updated@example.com"
    assert data["full_name"] == "John Updated"
    assert data["is_active"] is True


def test_update_user_not_found(client):
    """API should return 404 when user does not exist."""

    user_id = "00000000-0000-0000-0000-000000000000"

    response = client.patch(
        f"/api/v1/users/{user_id}",
        json={
            "full_name": "Updated Name",
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert "not found" in data["detail"].lower()


def test_update_user_duplicate_email(client):
    """API should return 409 for duplicate email."""

    client.post(
        "/api/v1/users/",
        json={
            "employee_id": "EMP-001",
            "email": "john@example.com",
            "full_name": "John Doe",
        },
    )

    second_response = client.post(
        "/api/v1/users/",
        json={
            "employee_id": "EMP-002",
            "email": "jane@example.com",
            "full_name": "Jane Doe",
        },
    )

    assert second_response.status_code == 201

    user_id = second_response.json()["user"]["id"]

    response = client.patch(
        f"/api/v1/users/{user_id}",
        json={
            "email": "john@example.com",
        },
    )

    assert response.status_code == 409

    data = response.json()

    assert "already exists" in data["detail"].lower()


def test_update_user_duplicate_employee_id(client):
    """API should return 409 for duplicate employee ID."""

    client.post(
        "/api/v1/users/",
        json={
            "employee_id": "EMP-001",
            "email": "john@example.com",
            "full_name": "John Doe",
        },
    )

    second_response = client.post(
        "/api/v1/users/",
        json={
            "employee_id": "EMP-002",
            "email": "jane@example.com",
            "full_name": "Jane Doe",
        },
    )

    assert second_response.status_code == 201

    user_id = second_response.json()["user"]["id"]

    response = client.patch(
        f"/api/v1/users/{user_id}",
        json={
            "employee_id": "EMP-001",
        },
    )

    assert response.status_code == 409

    data = response.json()

    assert "already exists" in data["detail"].lower()


def test_update_user_partial_update(client):
    """API should update only the supplied fields."""

    create_response = client.post(
        "/api/v1/users/",
        json={
            "employee_id": "EMP-001",
            "email": "john@example.com",
            "full_name": "John Doe",
        },
    )

    user_id = create_response.json()["user"]["id"]

    response = client.patch(
        f"/api/v1/users/{user_id}",
        json={
            "full_name": "John Updated",
        },
    )

    assert response.status_code == 200

    data = response.json()["user"]

    assert data["employee_id"] == "EMP-001"
    assert data["email"] == "john@example.com"
    assert data["full_name"] == "John Updated"
    assert data["is_active"] is True


def test_delete_user(client, db_session):
    """Test deleting an existing user."""

    create_response = client.post(
        "/api/v1/users/",
        json={
            "employee_id": "EMP-DELETE-001",
            "email": "delete@example.com",
            "full_name": "Delete User",
        },
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["user"]["id"]

    response = client.delete(f"/api/v1/users/{user_id}")

    assert response.status_code == 204
    assert response.content == b""

    # Verify the user no longer exists
    get_response = client.get(f"/api/v1/users/{user_id}")

    assert get_response.status_code == 404


def test_delete_user_not_found(client):
    """Test deleting a user that does not exist."""

    user_id = "00000000-0000-0000-0000-000000000000"

    response = client.delete(f"/api/v1/users/{user_id}")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
