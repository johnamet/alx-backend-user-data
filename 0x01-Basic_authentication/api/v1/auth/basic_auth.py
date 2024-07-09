#!/usr/bin/env python3
"""
The basic auth module
"""
import base64
from typing import TypeVar

from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    Basic auth class
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        if not authorization_header or \
                not isinstance(authorization_header, str) or \
                not authorization_header.startswith('Basic '):
            return None

        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str) \
            -> str:
        """
        Decode base64 encoded authorization header
        Args:
            base64_authorization_header:

        Returns:

        """

        decoded = None
        if (not base64_authorization_header or not
           isinstance(base64_authorization_header, str)):
            return None

        try:
            decoded = base64.b64decode(base64_authorization_header)
        except Exception:
            return None

        return decoded.decode('utf-8')

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extract user credentials from base64 encoded authorization header.
        Args:
            decoded_base64_authorization_header: The decoded authorization header string.

        Returns:
            A tuple (email, password) if extraction is successful, otherwise (None, None).
        """
        if not isinstance(decoded_base64_authorization_header, str) or ":" not in it:
            return None, None

        email, password = decoded_base64_authorization_header.split(":", 1)
        return email, password

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Create a user object from user credentials
        Args:
            user_email:
            user_pwd:

        Returns:

        """

        user = User.search({"email": user_email})

        if not user_email or not user_pwd:
            return None

        if (len(User.all()) == 0 or
                not len(user)):
            return None
        else:
            user = user[0]

        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Current user
        Args:
            request:

        Returns:

        """

        authorisation_header = (self.extract_base64_authorization_header
                                (request.headers.get('Authorization')))
        decoded_base64_authorization_header = \
            (self.decode_base64_authorization_header
                (authorisation_header))
        email, pwd = (self.extract_user_credentials
                      (decoded_base64_authorization_header))

        user = self.user_object_from_credentials(email, pwd)

        return user
