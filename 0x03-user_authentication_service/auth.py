#!/usr/bin/env python3
"""
Authentication module
"""
import uuid
from typing import TypeVar, Union

import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _generate_uuid() -> str:
    """
    Generate a random UUID
    :return: a str of random UUID
    """
    return str(uuid.uuid4())


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

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user.
        :param email:  Email of the user
        :param password: Password of user
        :return: User
        """

        try:
            user = self._db.find_user_by(email=email)

            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Checks if the email and password are valid.
        :param email: the email to check
        :param password: the password to check
        :return: boolean indicating if the email and password are valid
        """

        try:
            user = self._db.find_user_by(email=email)

            if user:
                return bcrypt.checkpw(password.encode('utf-8'),
                                      user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Creates a new session for the user.
        :param email: The email of the user
        :return: str of the session id
        """

        try:
            user = self._db.find_user_by(email=email)
            if user:
                setattr(user, "session_id", _generate_uuid())
            return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self,
                                 session_id: str)\
            -> Union[TypeVar("User"), None]:
        """
        Retrieve the user from the session id.
        :param session_id: The session id
        :return: The user or None if the session does not exist
        """

        try:
            user = self._db.find_user_by(session_id=session_id)

            if user:
                return user

        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy a session for the user.
        :param user_id: The user id
        :return: None
        """

        try:
            user = self._db.find_user_by(id=user_id)
            if user:
                setattr(user, "session_id", None)
                return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Resets the user password
        :param email: Email of the user
        :return: uuid
        """

        try:
            user = self._db.find_user_by(email=email)
            if user:
                token = _generate_uuid()
                self._db.update_user(user_id=user.id, reset_token=token)
                return token
            else:
                raise ValueError
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Resets the user password
        :param password:
        :param reset_token:
        :return:
        """

        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if user:
                hash_ = _hash_password(password)
                self._db.update_user(user_id=user.id,
                                     hashed_password=hash_, reset_token=None)
            else:
                raise ValueError
        except NoResultFound:
            raise ValueError
