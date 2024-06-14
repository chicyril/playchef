#!/usr/bin/env python3
"""Views package init."""
from flask import Blueprint

# Create blueprints
app_auth = Blueprint('app_auth', __name__)
app_views = Blueprint('app_views', __name__)

# Make views available to the app when importing package
from .auth_view import *
from .home_view import *
from .recipe_view import *
from .profile_view import *
