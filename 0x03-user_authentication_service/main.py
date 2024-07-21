#!/usr/bin/env python3
"""
Main file
"""

import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """
    Register a new user
    :param email:
    :param password:
    :return:
    """
    data = {
        "email": email,
        "password": password,
    }
    resp = requests.post(BASE_URL + "/users", data)
    if resp.status_code == 200:
        print("Registered successfully")
    else:
        print("Failed to register user")


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Login with wrong password
    :param email:
    :param password:
    :return:
    """

    resp = requests.post(BASE_URL + "/login",
                         data={"email": email, "password": password})
    if resp.status_code == 200:
        print("Login successfully")
    else:
        print("Failed to login")


def profile_unlogged():
    """

    :return:
    """

    resp = requests.get(BASE_URL + "/profile")

    if resp.status_code == 200:
        print("Profile unlogged successfully")


def log_in(email: str, password: str) -> str:
    """
    log in a new user
    :param email:
    :param password:
    :return:
    """

    data = {
        "email": email,
        "password": password,
    }

    resp = requests.post(BASE_URL + "/sessions", data=data)

    if resp.status_code == 200:
        return resp.cookies.get("session_id")


def profile_logged(session_id: str) -> None:
    """
    Check profile
    :param session_id:
    :return:
    """
    cookies = {
        "session_id": session_id
    }
    req = requests.get(BASE_URL + "/profile", cookies=cookies)


def log_out(session_id: str) -> None:
    """
    log out
    :param session_id:
    :return:
    """
    cookies = {
        "session_id": session_id
    }
    req = requests.delete(BASE_URL + "/sessions", cookies=cookies)


def reset_password_token(email: str) -> str:
    """
    reset password
    :param email:
    :return:
    """

    req = requests.post(BASE_URL + "/reset_password", data={"email": email})

    if req.status_code == 200:
        return req.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    reset password
    :param email:
    :param reset_token:
    :param new_password:
    :return:
    """
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }

    req = requests.put(BASE_URL + "/reset_password", data=data)


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
