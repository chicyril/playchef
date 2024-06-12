#!/usr/bin/env python3
"""
THIS MODULE SHOULD ALWAYS BE IN THE APP PACKAGE OR AT THE SAME DIRECTORY LEVEL
AS THE APP MODULE.

This module contains default configuration key-val pair for testing the app.
Edit values for existing keys, add new keys = vals to any of the sections in
the class `Default`, or create new sections `# [SECTION NAME]` with keys = vals
to configure to your preferrence.

Note: If existing keys is duplicated here or in any other config file read by
    the app, the last read values for the keys overide the previous ones and is
    used by the app. This module is read first by app though.
"""
import os
from os import getenv
from urllib.parse import quote_plus


class Default:
    """Test configuration"""
    # [APP]
    TESTING = True
    SECRET_KEY = getenv('PLAYCHEF_SECRET_KEY', '76f1b197713RandoM369e13508549')
    HOST = getenv('HOST', '0.0.0.0')
    PORT = getenv('PORT', 5000)

    # [DATABASE]
    DB_HOST = getenv('DB_HOST', 'localhost')
    DB_NAME = getenv('DB_NAME', 'playchef_db')
    DB_USER = getenv('DB_USER', 'playchef_dev')
    DB_PASSWORD = quote_plus(getenv('DB_PASSWORD', 'Devchef1_'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # [STATIC FOLDERS]
    MAX_CONTENT_PATH = 1024 * 1024
    RECIPE_IMG_FOLDER = os.path.join(os.path.dirname(__file__),
                                     'static/recipe_imgs')
    PROFILE_PIC_FOLDER = os.path.join(os.path.dirname(__file__),
                                      'static/profile_pics')

    if not os.path.exists(RECIPE_IMG_FOLDER):
        os.makedirs(RECIPE_IMG_FOLDER)
    if not os.path.exists(PROFILE_PIC_FOLDER):
        os.makedirs(PROFILE_PIC_FOLDER)
