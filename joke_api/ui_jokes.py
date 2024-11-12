#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
joke_api /jokes UI blueprint
"""
from flask import (
    Blueprint, request, render_template
)
from .api_categories import category_get
from .api_jokes import joke_get, joke_set, joke_delete, joke_random

BP = Blueprint('ui_jokes', __name__, url_prefix='/jokes')

@BP.route("/", methods=["GET"])
def ui_form_jokes():
    """
    This function lists all jokes
    """
    # get _all_ the jokes
    jokes = joke_get(0)
    # get category
    categories = category_get(0)
    # render jokes in HTML template
    return render_template("jokes.html", result=jokes, categories=categories)

@BP.route("/create", methods=["GET", "POST"])
def ui_form_create_joke():
    """
    This function presents the form to create jokes
    and returns the API result
    """
    if request.method == "POST":
        # create joke
        msg = {
            "link": "/jokes",
            "link_text": "back",
            "text": "Joke could not be created!"
        }
        if joke_set(
                request.form["category_id"],
                request.form["joke_text"],
                request.form["joke_rank"]
            ):
            msg['text'] = "Joke created!"
        result = render_template("message.html", message=msg)
    else:
        # show form
        categories = category_get(0)
        result = render_template("joke_create.html", categories=categories)
    return result

@BP.route("/<int:joke_id>", methods=["GET"])
def ui_form_joke(joke_id):
    """
    This function displays a particular joke

    :param joke_id: joke ID
    :type joke_id: int
    """
    # display a particular joke
    result = joke_get(joke_id)["results"][0]
    return render_template("joke.html", joke=result)

@BP.route("/random", methods=["GET"])
def ui_form_joke_random():
    """
    This function shows a random joke
    """
    # display a random joke
    random_joke = joke_random()["results"][0]
    joke_category = category_get(random_joke["category_id"])
    return render_template(
        "joke.html", joke=random_joke, category=joke_category["results"][0]
    )

@BP.route("/random/<int:category_id>", methods=["GET"])
def ui_form_joke_random_category(category_id):
    """
    This function shows a random joke from a particular category
    """
    # display a random joke from a category
    result = joke_random(category_id)["results"][0]
    return render_template("joke.html", joke=result)

@BP.route("/delete/<int:joke_id>", methods=["GET"])
def ui_form_delete_joke(joke_id):
    """
    This function deletes a particular joke

    :param joke_id: joke ID
    :type joke_id: int
    """
    # try to delete joke
    msg = {
        "link": "/jokes",
        "link_text": "back",
        "text": "Joke could not be deleted!"
    }
    if joke_delete(joke_id):
        msg['text'] = "Joke deleted!"
    return render_template("message.html", message=msg)

@BP.route("/edit/<int:joke_id>", methods=["GET", "POST"])
def ui_form_edit_joke(joke_id):
    """
    This function presents the form to edit jokes and returns form
    data to the API

    :param joke_id: joke ID
    :type joke_id: int
    """
    if request.method == "POST":
        # edit joke
        msg = {
            "link": "/jokes",
            "link_text": "back",
            "text": "Joke could not be edited!"
        }
        if joke_set(
                request.form["category_id"],
                request.form["joke_text"],
                request.form["joke_rank"],
                joke_id
            ):
            msg['text'] = "Joke edited!"
        result = render_template("message.html", message=msg)
    else:
        # show form, preselect values
        try:
            result = joke_get(joke_id)["results"][0]
            categories = category_get(0)
            result = render_template("joke_edit.html", joke=result, categories=categories)
        except IndexError:
            result = render_template("joke_nonexist.html")
    return result
