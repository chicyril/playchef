#!/usr/bin/env python3
"""This module contains abstraction for the database storage."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Model, Base


class Storage:
    """Definition of the storage class."""

    def __init__(self, app):
        """Initialize database: connect to db, create schemas and session."""

        db_url = app.config.get('SQLALCHEMY_DATABASE_URI')
        self.__engine = create_engine(db_url, pool_pre_ping=True)

        if app.config.get('TESTING'):
            Base.metadata.drop_all(self.__engine)

        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

        Base.query = self.__session.query_property()

    def add(self, obj):
        """Add an object to the database session."""
        if isinstance(obj, Model):
            self.__session.add(obj)

    def delete(self, obj=None):
        """Delete an object from the database session."""
        if obj is not None:
            self.__session.delete(obj)

    def commit(self):
        """Persist changes in session to database table."""
        self.__session.commit()

    def rm_session(self):
        """Remove the current database session."""
        self.__session.remove()
