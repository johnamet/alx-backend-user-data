#!/usr/bin/env python3
"""
User session db
"""
from models.base import Base


class UserSession(Base):
    """
    User session
    """

    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("id")
        self.session_id = kwargs.get("session_id")