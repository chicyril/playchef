#!/usr/bin/env python3
"""This module contains abstraction for the database storage."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Model, Base


class Storage:
    """Definition of the storage class."""

    def __init__(self, app):
        """
        Initialize database:
            connect to database server, create schemas and session.
        """

        # Create database url with configs from the app.
        db_url = app.config.get('SQLALCHEMY_DATABASE_URI')
        self.__engine = create_engine(db_url, pool_pre_ping=True)

        # Reset the database everytime the app is run in testing mode,
        # i.e TESTING = True in app's config.
        if app.config.get('TESTING'):
            Base.metadata.drop_all(self.__engine)

        # Create table schemas in database.
        Base.metadata.create_all(self.__engine)

        # Create a database scoped session.
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

        # Add query attribute to Base to enable easy query of the database with
        # class names.
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
