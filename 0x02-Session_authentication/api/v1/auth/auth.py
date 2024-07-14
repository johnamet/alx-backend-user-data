#!/usr/bin/env python3
"""
The Authentication Module
"""
from typing import List, TypeVar
import os


class Auth:
    """
    The Basic Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Defines path that requires auth
        """

        if not excluded_paths or not path:
            return True

        path = path.rstrip('/')

        normalised_excluded_paths = {p.rstrip('/') for p in excluded_paths}

        for excluded_path in normalised_excluded_paths:
            if excluded_path.endswith("*"):
                path_name = path.split('/')[-1]
                excluded_path_name = excluded_path.split('/')[-1][:-1]
                if path_name.startswith(excluded_path_name):
                    return False

        return not (path in normalised_excluded_paths)

    def authorization_header(self, request=None) -> str:
        """
        Flask request object
        """
        if request is None or request.headers.get('Authorization') is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Flask request object for current user
        """

        return None

    def session_cookie(self, request=None):
        """
        Flask request object for session cookie
        """

        if request is None:
            return None

        session_name = os.environ.get('SESSION_NAME')

        return request.cookies.get(session_name)
