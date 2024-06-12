#!/usr/bin/env pythonn3
"""
This module defines form implementation for handling recipe creation and
editing.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FieldList, FormField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Optional
from flask_wtf.file import FileField, FileAllowed
from models import Category


class IngredientForm(FlaskForm):
    name = StringField('Ingredient',
                       validators=[DataRequired(), Length(min=2, max=100)])


class StepForm(FlaskForm):
    description = TextAreaField('Step',
                                validators=[DataRequired(), Length(min=2)])


class RecipeForm(FlaskForm):
    name = StringField('Recipe Name',
                       validators=[DataRequired(), Length(min=2, max=200)])

    description = TextAreaField('Description',
                                validators=[Length(max=1024), Optional()])

    image = FileField('Choose Image',
                      validators=[FileAllowed(['jpg', 'png']), Optional()])

    ingredients = FieldList(FormField(IngredientForm), min_entries=1)

    steps = FieldList(FormField(StepForm), min_entries=1)

    categories = SelectMultipleField('Categories', choices=[],
                                     validate_choice=True)

    new_category = StringField('New Category', validators=[Optional()])

    submit = SubmitField('Create Recipe')

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.categories.choices = [(category.id, category.name)
                                   for category in Category.query.all()]
