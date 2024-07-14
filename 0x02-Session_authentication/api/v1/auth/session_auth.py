#!/usr/bin/env python3
"""
The session auth module
"""
import uuid

from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
    Session Auth
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str) -> str | None:
        """
        Create a session
        :param user_id: user id is the id of the user
        :return: session id
        """

        if not user_id or not isinstance(user_id, str):
            return None

        session_id = uuid.uuid4()

        self.user_id_by_session_id[session_id] = user_id

        return session_id
