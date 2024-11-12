#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
joke_api /categories UI blueprint
"""
import logging
from flask import (
    Blueprint, request, render_template
)
from .api_categories import category_get, category_set, category_delete

BP = Blueprint('ui_categories', __name__, url_prefix='/categories')

@BP.route("/", methods=["GET"])
def ui_form_categories():
    """
    This function lists all categories
    """
    # get _all_ the categories
    categories = category_get(0)
    logging.error(categories)
    # render categories in HTML template
    return render_template("categories.html", result=categories)

@BP.route("/create", methods=["GET", "POST"])
def ui_form_create_category():
    """
    This function presents the form to create categories
    and returns the API result
    """
    if request.method == "POST":
        # create category
        msg = {
            "link": "/categories",
            "link_text": "back",
            "text": "Category could not be created!"
        }
        if category_set(
                request.form["name"]
            ):
            msg['text'] = "Category created!"
        result = render_template("message.html", message=msg)
    else:
        # show form
        result = render_template("category_create.html")
    return result

@BP.route("/delete/<int:category_id>", methods=["GET"])
def ui_form_delete_category(category_id):
    """
    This function deletes a particular category

    :param category_id: category ID
    :type category_id: int
    """
    # try to delete category
    msg = {
        "link": "/categories",
        "link_text": "back",
        "text": "Category could not be deleted!"
    }
    if category_delete(category_id):
        msg['text'] = "Category deleted!"
    return render_template("message.html", message=msg)

@BP.route("/edit/<int:category_id>", methods=["GET", "POST"])
def ui_form_edit_category(category_id):
    """
    This function presents the form to edit categories and returns form
    data to the API

    :param category_id: category ID
    :type category_id: int
    """
    if request.method == "POST":
        # edit category
        msg = {
            "link": "/categories",
            "link_text": "back",
            "text": "Category could not be edited!"
        }
        if category_set(
                request.form["category_name"],
                category_id,
                category_newid=request.form["category_id"]
            ):
            msg['text'] = "Category edited!"
        result = render_template("message.html", message=msg)
    else:
        # show form, preselect values
        try:
            category_name = category_get(category_id)["results"][0]
            result = render_template("category_edit.html", category=category_name)
        except IndexError:
            result = render_template("category_nonexist.html")
    return result
