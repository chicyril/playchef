#!/usr/bin/env python3
"""This module defines a flask app factory function, and creates and and a
created flask app instance.
"""
import os
from flask import Flask


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

    @app.teardown_appcontext
    def remove_session(e):
        """Remove the current scoped session after a request."""
        app.db.rm_session()

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 error."""
        return 'What have you done?', 404

    return app


app = create_app()
