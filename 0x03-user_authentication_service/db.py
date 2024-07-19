"""DB module"""
from typing import TypeVar

from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from sqlalchemy.orm import sessionmaker, Session

from user import Base, User


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance."""
        self._engine = create_engine("sqlite:///a.db", echo=True)
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

    def add_user(self, email: str,
                 hashed_password: str) -> TypeVar('User'):
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

    def find_user_by(self, **kwargs) -> TypeVar('User'):
        """
        Find a user by email.
        :param **kwargs: The email of the user.
        :return: user
        """

        try:
            user = (self._session.query(User)
                    .filter_by(**kwargs).one())
            return user
        except NoResultFound as e:
            raise NoResultFound from e
        except InvalidRequestError as e:
            raise InvalidRequestError from e

    def update_user(self, user_id: int,
                    **kwargs):
        """
        Update a user.
        :param kwargs: the keyword arguments of the user.
        :return: user
        """

        try:
            user = self.find_user_by(id=user_id)
        except Exception as e:
            raise ValueError

        try:
            for key, value in kwargs.items():
                setattr(user, key, value)

            self._session.add(user)
            self._session.commit()
        except Exception as e:
            self._session.rollback()
