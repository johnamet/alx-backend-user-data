#!/usr/bin/env python3
"""DB module"""
from typing import Type

from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker, Session

from user import Base, User


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance."""
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)

        try:
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e

        return user

    def find_user_by(self, **kwargs) -> Type[User]:
        """
        Find a user by attributes.

        Args:
            **kwargs: The attributes to filter the user by.

        Returns:
            User: The found User object.

        Raises:
            NoResultFound: If no user is found.
            InvalidRequestError: If the query is invalid.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound as e:
            raise NoResultFound from e
        except InvalidRequestError as e:
            raise InvalidRequestError from e

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: The attributes to update.

        Raises:
            ValueError: If the user is not found.
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError("User not found")

        for key, value in kwargs.items():
            setattr(user, key, value)

        self._session.add(user)

        try:
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e
