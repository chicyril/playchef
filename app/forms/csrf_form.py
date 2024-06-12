#!/usr/bin/env python3
"""A form class for just to pass csrf token to the template."""
from flask_wtf import FlaskForm


# Flask form subclass used just to pass csrf token to the template.
class CSRFForm(FlaskForm):
    pass
