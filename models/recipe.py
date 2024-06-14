#!/usr/bin/env python3
"""This module contains the class definitions for recipe, category, ingredient
and steps, and recipe-category secondary table."""
from sqlalchemy import Column, String, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from models.base_model import Model, Base
from models.user_fav_recipe import favorites_table


# Recipe_category many-to-many table.
recipe_categories = Table('recipe_categories', Base.metadata,
                          Column('category_id', String(36),
                                 ForeignKey('categories.id'),
                                 primary_key=True),
                          Column('recipe_id', String(36),
                                 ForeignKey('recipes.id'),
                                 primary_key=True))


class Category(Model, Base):
    """The category class definition."""
    __tablename__ = 'categories'
    name = Column(String(100), nullable=False, unique=True)
    user_id = Column(String(36), ForeignKey('users.id'))

    user = relationship('User', back_populates='categories')

    recipes = relationship('Recipe', secondary=recipe_categories,
                           back_populates='categories')


class Recipe(Model, Base):
    """The recipe class definition."""
    __tablename__ = 'recipes'
    name = Column(String(200), nullable=False)
    user_id = Column(String(36), ForeignKey('users.id'))
    description = Column(Text)
    image = Column(String(40), nullable=False, default='recipe_default.jpg')

    user = relationship('User', back_populates='recipes')

    categories = relationship('Category', secondary=recipe_categories,
                              back_populates='recipes')

    ingredients = relationship('Ingredient', back_populates='recipe',
                               cascade='all, delete-orphan')

    steps = relationship('Step', back_populates='recipe',
                         cascade='all, delete-orphan')

    favorited_by = relationship('User', secondary=favorites_table,
                                back_populates='favorites')


class Ingredient(Model, Base):
    """The ingredient class definition."""
    __tablename__ = 'ingredients'
    name = Column(String(100), nullable=False)
    recipe_id = Column(String(36), ForeignKey('recipes.id'), nullable=False)
    recipe = relationship('Recipe', back_populates='ingredients')


class Step(Model, Base):
    """Steps class definition."""
    __tablename__ = 'steps'
    description = Column(Text, nullable=False)
    recipe_id = Column(String(36), ForeignKey('recipes.id'), nullable=False)
    recipe = relationship('Recipe', back_populates='steps')
