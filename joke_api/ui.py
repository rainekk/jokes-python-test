#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
joke_api / UI blueprint
"""
from flask import (
    Blueprint, render_template, send_from_directory
)

BP = Blueprint('ui', __name__, url_prefix='/')

@BP.route("/")
def index():
    """
    This function simply presents the main page
    """
    return render_template("index.html")

@BP.route('/css/<path:path>')
def send_js(path):
    """
    This function returns the CSS
    """
    return send_from_directory('templates/css', path)
