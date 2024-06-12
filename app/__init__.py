#!/usr/bin/env python3
"""This module defines a flask app factory function, and creates and and a
created flask app instance.
"""
import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from models import Storage, Category, User


def create_instance_config(path):
    """Create the instance config file with some commented out default configs.
    """

    some_configs = """
## Uncomment keys below and edit values as needed.

## [APP]
# TESTING = False
# SECTRETE_KEY = "You'll never guess"
# HOST = "localhost"
# PORT = 5000

## [DATABASE]
# DB_HOST = "database_host"
# DB_NAME = "database_name"
# DB_USER = "admin"
# DB_PASSWORD = 'admin_passwd'
"""

    with open(path, 'w') as config_file:
        config_file.write(some_configs)


def create_default_categories(app):
    """Create predefined categories for the app."""

    predefined_categories = ['breakfast', 'lunch', 'dinner']
    existing_predef_cats = [category.name for category in Category.query.all()]
    if not set(predefined_categories).issubset(set(existing_predef_cats)):
        for category_name in predefined_categories:
            if category_name not in existing_predef_cats:
                category = Category(name=category_name)
                app.db.add(category)
        app.db.commit()
    app.db.rm_session()


# Define a factory function for creating flask app instance.
def create_app():
    """A flask app factory function"""

    app = Flask(__name__, instance_relative_config=True)

    # Make sure the instance folder is created and then create instance config
    # file.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    instance_config_path = os.path.join(app.instance_path, 'instance_cnfg.py')
    if not os.path.isfile(instance_config_path):
        create_instance_config(instance_config_path)

    # Read default config from a class and then from the instance config file.
    app.config.from_object('app.app_config.Default')
    app.config.from_pyfile('instance_cnfg.py', silent=True)

    # Read dabase configurations from the app's config and create the database
    # url string which is then stored in the app's config.
    db_usr = app.config.get('DB_USER')
    db_passwd = app.config.get('DB_PASSWORD')
    db_host = app.config.get('DB_HOST')
    db_name = app.config.get('DB_NAME')

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f'mysql+mysqldb://{db_usr}:{db_passwd}@{db_host}/{db_name}')

    # Initialize csfr with app to help protect forms that are dynamically
    # created using html and not wtforms.
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Initialize a database(Storage model) object for the app and create default
    # categories.
    app.db = Storage(app)
    create_default_categories(app)

    # Register blueprints with the app.
    from app.views import app_auth, app_views
    app.register_blueprint(app_auth)
    app.register_blueprint(app_views)

    # Create a bcrypt instance as attribute of app for hashing user password.
    app.bcrypt = Bcrypt(app)

    # Create login_manager attribute for managing user session
    app.login_manager = LoginManager(app)
    app.login_manager.login_view = 'app_auth.login'
    app.login_manager.login_message_category = 'info'

    # Load the user object from the database during user session.
    @app.login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # Remove the current database session after each request.
    @app.teardown_appcontext
    def remove_session(e):
        """Remove the current scoped session after a request."""
        app.db.rm_session()

    # Handle all 404 errors.
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 error."""
        return 'What have you done?', 404

    return app


app = create_app()
