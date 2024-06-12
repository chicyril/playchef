#!/usr/bin/env python3
"""Defines a many-to-many relationship table for users' favorite recipes."""
from sqlalchemy import Column, String, ForeignKey, Table
from models.base_model import Base

favorites_table = Table('favorites', Base.metadata,
                        Column('user_id', String(60),
                               ForeignKey('users.id'),
                               primary_key=True),
                        Column('recipe_id', String(60),
                               ForeignKey('recipes.id'),
                               primary_key=True))
