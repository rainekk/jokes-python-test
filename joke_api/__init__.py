#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
joke_api application
"""
import os
from flask import Flask

from . import db
from . import api_categories
from . import api_jokes
from . import ui
from . import ui_categories
from . import ui_jokes

def create_app(test_config=None):
    """
    This functions creates and configures the app
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'joke_api.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # add database
    db.init_app(app)

    # add category API calls
    app.register_blueprint(api_categories.BP)

    # add joke API calls
    app.register_blueprint(api_jokes.BP)

    # add UI
    app.register_blueprint(ui.BP)
    app.register_blueprint(ui_categories.BP)
    app.register_blueprint(ui_jokes.BP)

    return app
