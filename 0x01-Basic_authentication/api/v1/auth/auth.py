#!/usr/bin/env python3
"""
The Authentication Module
"""
from flask import request
from typing import List


class Auth:
    """
    The Basic Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Defines path that requires auth
        """

        return False

    def authorization_header(self,request=None) -> str:
        """
        Flask request object
        """

        return None


    def current_user(self, request=None) -> TypeVar('User'):
        """
        Flask request object for current user
        """

        return None

