#!/usr/bin/env python3
"""Contains views for sign-up and login."""
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from app.views import app_auth
from app.forms.auth_form import SignUpForm, LoginForm
from models import User


@app_auth.route('/sign-up', methods=['GET', 'POST'], strict_slashes=False)
def signup():
    """End point function for signup."""
    if current_user.is_authenticated:
        return redirect(url_for('app_views.home'))
    form = SignUpForm()
    if form.validate_on_submit():
        password_hash = current_app.bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=password_hash)
        current_app.db.add(user)
        current_app.db.commit()
        flash(f'Sign up successful! {form.username.data} is logged in',
              'success')
        return redirect(url_for('app_auth.login'))
    return render_template('sign_up.html', title='Sign Up', form=form)


@app_auth.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """End point for login."""
    if current_user.is_authenticated:
        return redirect(url_for('app_views.home'))

    next_page = request.args.get('next')

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and \
            current_app.bcrypt.check_password_hash(user.password,
                                                   form.password.data):

            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')

            if next_page and next_page != '/None':
                return redirect(next_page)
            return redirect(url_for('app_views.home'))

        flash('Invalid email or password', 'danger')

    return render_template('login.html', title='Log In',
                           form=form, next=next_page)


@app_auth.route('/logout', strict_slashes=False)
@login_required
def logout():
    """End point for logout."""
    logout_user()
    return redirect(url_for('app_auth.login'))
