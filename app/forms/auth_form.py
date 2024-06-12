#!/usr/bin/env pythonn3
"""This module defines forms and form validation implementation for sign-up
and login."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User


class SignUpForm(FlaskForm):
    """Sign-up form class."""
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """Validate username from database."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one')

    def validate_email(self, email):
        """Validate username from database."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one')


class LoginForm(FlaskForm):
    """Login form class."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=4)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
