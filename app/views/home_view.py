#!/usr/bin/env python3
"""Contains views for home routes."""
from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from app.views import app_views
from models import Category
from app.forms.csrf_form import CSRFForm


@app_views.route('/', strict_slashes=False)
def landing():
    """Endpoint function for landing page"""
    if current_user.is_authenticated:
        return redirect(url_for('app_views.home'))
    return render_template('landing.html')


@app_views.route('/home', strict_slashes=False)
@login_required
def home():
    """Endpoint for home."""
    csrf_form = CSRFForm()
    categories = Category.query.all()
    categories = [category.name for category in categories
                  if category.name not in ['breakfast', 'lunch', 'dinner']]
    return render_template('home.html', categories=categories, form=csrf_form)
