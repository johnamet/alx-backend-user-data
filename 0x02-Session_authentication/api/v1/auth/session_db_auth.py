#!/usr/bin/env python3
"""
Authentication
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    Db for session
    """

    def create_session(self, user_id=None):
        """
        create a session
        """
        if not user_id:
            return

        user_session = super().create_session(user_id)

        if not user_session:
            return

        user_session_obj = UserSession()

        user_session_obj.user_id = user_id
        user_session_obj.session_id = user_session

        user_session_obj.save()

    def user_id_for_session_id(self, session_id=None):
        """
        user id for session
        """

        if not session_id:
            return None

        user_session = UserSession.get(session_id)

        if not user_session:
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """
        destroy session or logout
        """

        if not request:
            return False

        session_id = self.session_cookie(request)

        if not session_id:
            return False

        user_session = UserSession.get(session_id)

        if not user_session:
            return False

        user_session.remove()

        return True
