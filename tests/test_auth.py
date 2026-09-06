from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_login_success():
    response = client.post(
        "/login",
        json={
            "username": "aidana",
            "password": "testpassword",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password():
    response = client.post(
        "/login",
        json={
            "username": "aidana",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401


def test_profile_without_token():
    response = client.get("/profile")

    assert response.status_code == 401


def test_profile_with_access_token():
    login_response = client.post(
        "/login",
        json={
            "username": "aidana",
            "password": "testpassword",
        },
    )

    access_token = login_response.json()["access_token"]

    response = client.get(
        "/profile",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 200
    assert response.json()["username"] == "aidana"


def test_refresh_token():
    login_response = client.post(
        "/login",
        json={
            "username": "aidana",
            "password": "testpassword",
        },
    )

    refresh_token = login_response.json()["refresh_token"]

    response = client.post(
        "/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_refresh_token_cannot_access_profile():
    login_response = client.post(
        "/login",
        json={
            "username": "aidana",
            "password": "testpassword",
        },
    )

    refresh_token = login_response.json()["refresh_token"]

    response = client.get(
        "/profile",
        headers={
            "Authorization": f"Bearer {refresh_token}",
        },
    )

    assert response.status_code == 401