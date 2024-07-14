#!/usr/bin/env python3
"""
Session exp date
"""
import datetime
import os

from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    Expiration class
    """
    session_dictionary = {}

    def __init__(self):
        super().__init__()

        self.session_duration = 0

        try:
            self.session_duration = int(os.getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id = None) -> str:
        """
        Creates a new session
        """
        session_id = None

        if not user_id:
            return None

        try:
            session_id = super().create_session(user_id)
        except Exception:
            return None
        self.session_dictionary["user_id"] = user_id
        self.session_dictionary[session_id] = self.user_id_by_session_id
        self.session_dictionary["created_at"] = datetime.datetime.now()

        return session_id

    def user_id_for_session_id(self, session_id = None) -> str:
        """
        user id for session id
        """

        if not session_id:
            return None

        if session_id not in self.user_id_by_session_id:
            return None

        if self.session_duration <= 0:
            return self.session_dictionary["user_id"]

        if not "created_at" in self.session_dictionary:
            return None

        total_sec = (self.session_dictionary.get("created_at") +
                     datetime.timedelta(seconds=self.session_duration))

        if datetime.datetime.now() > total_sec:
            return None

        return self.session_dictionary["user_id"]
