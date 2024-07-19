#!/usr/bin/env python3
"""
The user class module
"""
from typing import Dict, Any, List

from sqlalchemy import String, Integer, Column
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    The user entity
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), unique=True, nullable=False, )
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
