#!/usr/bin/env python3
"""
The session auth module
"""
import uuid

from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    Session Auth
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str) -> str:
        """
        Create a session
        :param user_id: user id is the id of the user
        :return: session id
        """

        if not user_id or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str) -> str:
        """
        Get the user id of the session
        :param session_id: session id
        :return: user id
        """

        if not session_id or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        get current user
        """
        session_id = self.session_cookie(request)

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return None

        user = User.get(user_id)

        if not user:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        destroy session or logout
        """

        if not request:
            return False

        session_id = self.session_cookie(request)

        if not session_id:
            return False

        if not self.user_id_for_session_id(session_id):
            return False

        del self.user_id_by_session_id[session_id]

        return True
