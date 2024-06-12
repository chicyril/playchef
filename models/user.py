#!/usr/bin/env python3
"""This module contains the user class definition."""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from models.base_model import Model, Base
from models.recipe import Recipe
from models.user_fav_recipe import favorites_table


class User(Model, Base, UserMixin):
    """The user class definition."""
    __tablename__ = 'users'
    username = Column(String(30), unique=True, nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    display_pic = Column(String(40), nullable=False, default='default.jpg')

    recipes = relationship('Recipe', back_populates='user',
                           order_by=Recipe.created_at)

    categories = relationship('Category', back_populates='user')

    favorites = relationship('Recipe', secondary=favorites_table,
                             back_populates='favorited_by')
