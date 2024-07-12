#!/usr/bin/env python3
"""
The Authentication Module
"""
from typing import List, TypeVar


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

        # if not (path in normalised_excluded_paths):
        #     return True

        for excluded_path in normalised_excluded_paths:
            if excluded_path.endswith("*"):
                path_name = path.split('/')[-1]
                excluded_path_name = excluded_path.split('/')[-1][:-2]
                if excluded_path_name in path_name:
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
