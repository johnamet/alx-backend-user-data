#!/usr/bin/env python3
"""
Authentication module
"""
from typing import TypeVar

import bcrypt

from db import DB


def _hash_password(password: str) -> bytes:
    """
    Hashes password.
    :param password: the password to hash
    :return: the base64 encoded password
    """

    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    return hashed_pwd


class Auth:
    """
    Auth class to interact with the authentication service.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar("User"):
        """
        Register a new user.
        :param email:  Email of the user
        :param password: Password of the user
        :return: The User
        """

        try:
            user = self._db.find_user_by(email=email)

            if not user:
                user = self._db.add_user(email, _hash_password(password))
                return user
            else:
                raise ValueError(f"User {email} already exists")
        except Exception as e:
            raise ValueError(f"User {email} already exists")
