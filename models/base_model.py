#!/usr/bin/env python3
"""This module defines the base model for all other models."""
from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Model:
    """This is the super model which other models inherit from."""
    id = Column(String(36), primary_key=True,
                unique=True, default=lambda: str(uuid4()))

    created_at = Column(DateTime, nullable=False,
                        default=lambda: datetime.now(timezone.utc))

    updated_at = Column(DateTime, nullable=False,
                        default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __init__(self, **kwargs):
        if kwargs:
            for key, val in kwargs.items():
                setattr(self, key, val)

    def dicto(self):
        """Return the dictionary representation of an object."""
        dic = self.__dict__.copy()
        if '_sa_instance_state' in dic:
            del dic['_sa_instance_state']
        dic['created_at'] = self.created_at.isoformat()
        dic['updated_at'] = self.updated_at.isoformat()
        return dic

    def __repr__(self):
        return f'{type(self).__name__}({self.id})'
