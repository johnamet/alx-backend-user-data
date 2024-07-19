#!/usr/bin/env python3
"""
Main file
"""
import requests

BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    response = requests.post(f"{BASE_URL}/users",
                             json={"email": email, "password": password})
    assert response.status_code == 201,\
        f"Expected status code 201, got {response.status_code}"
    payload = response.json()
    assert payload["email"] == email,\
        f"Expected email {email}, got {payload['email']}"
    assert (payload["message"] ==
            "user created"), (f"Expected message 'user created', "
                              f"got {payload['message']}")


def log_in_wrong_password(email: str, password: str) -> None:
    response = requests.post(f"{BASE_URL}/sessions",
                             json={"email": email,
                                   "password": password})
    assert response.status_code == 401,\
        (f"Expected status code 401, got"
         f"{response.status_code}")


def log_in(email: str, password: str) -> str:
    response = requests.post(f"{BASE_URL}/sessions",
                             json={"email": email, "password": password})
    assert response.status_code == 200, (f"Expected status code 200, "
                                         f"got {response.status_code}")
    payload = response.json()
    assert payload["email"] == email,\
        f"Expected email {email}, got {payload['email']}"
    assert (payload["message"] ==
            "logged in"), (f"Expected message"
                           f"'logged in', got {payload['message']}")
    session_id = response.cookies.get("session_id")
    assert session_id is not None, "Expected session_id in cookies"
    return session_id


def profile_unlogged() -> None:
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403,\
        f"Expected status code 403, got {response.status_code}"


def profile_logged(session_id: str) -> None:
    response = requests.get(f"{BASE_URL}/profile",
                            cookies={"session_id": session_id})
    assert response.status_code == 200, (f"Expected status code 200, "
                                         f"got {response.status_code}")
    payload = response.json()
    assert "email" in payload, "Expected 'email' in response payload"


def log_out(session_id: str) -> None:
    response = requests.delete(f"{BASE_URL}/sessions",
                               cookies={"session_id": session_id})
    assert response.status_code == 200,\
        f"Expected status code 200, got {response.status_code}"


def reset_password_token(email: str) -> str:
    response = requests.post(f"{BASE_URL}/reset_password",
                             json={"email": email})
    assert response.status_code == 200,\
        f"Expected status code 200, got {response.status_code}"
    payload = response.json()
    assert payload["email"] == email,\
        f"Expected email {email}, got {payload['email']}"
    reset_token = payload.get("reset_token")
    assert reset_token is not None, "Expected reset_token in response"
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    response = requests.put(f"{BASE_URL}/reset_password", json={
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    })
    assert response.status_code == 200,\
        f"Expected status code 200, got {response.status_code}"
    payload = response.json()
    assert payload["email"] == email,\
        f"Expected email {email}, got {payload['email']}"
    assert (payload["message"] ==
            "Password updated"),\
        f"Expected message 'Password updated', got {payload['message']}"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
