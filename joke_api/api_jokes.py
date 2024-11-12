#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
joke_api /api/jokes blueprint
"""
import json
import logging
import sqlite3
import random

from flask import (
    Blueprint, Response, request
)

from .db import get_db
from .api_shared import return_result, get_category_id_by_name

BP = Blueprint('api_jokes', __name__, url_prefix='/api/jokes')

def joke_get(joke_id):
    """
    This function retrieves a joke's information

    :param joke_id: joke ID
    :type joke_id: int
    """
    database = get_db()
    try:
        if joke_id > 0:
            # return one particular joke
            jokes = database.execute(
                "SELECT * FROM jokes WHERE joke_id=?;",
                (joke_id,)
            )
        else:
            # return all jokes
            jokes = database.execute("SELECT * FROM jokes;")

        # return result
        return {"results": [dict(row) for row in jokes.fetchall()]}
    except sqlite3.Error as err:
        logging.error('Unable to get joke: %s', err)
        return False

def joke_set(category_id, joke_text, joke_rank, joke_id=None):
    """
    This function creates/updates a joke

    :param category_id: category ID
    :type category_id: int
    :param joke_text: joke text
    :type joke_text: str
    :param joke_rank: joke ranking
    :type joke_rank: int
    :param joke_id: joke ID
    :type joke_id: int
    """
    database = get_db()
    try:
        if joke_id:
            # update existing joke
            database.execute(
                """UPDATE jokes SET category_id=?, joke_text=?, joke_rank=?
                WHERE joke_id=?""",
                (category_id, joke_text, joke_rank, joke_id,)
            )
            database.commit()
            logging.info('Updated joke %s', joke_id)
            result = True
        else:
            # create new joke
            database.execute(
                """INSERT INTO jokes (category_id, joke_text, joke_rank)
                VALUES (?, ?, ?)""",
                (category_id, joke_text, joke_rank,)
            )
            database.commit()
            logging.info('Created joke %s', joke_text)
            result = True
        return result
    except sqlite3.Error as err:
        logging.error('Unable to create/update joke: %s', err)
        return False

def joke_delete(joke_id):
    """
    Deletes a joke.

    :param joke_id: joke ID
    :type joke_id: int
    """
    database = get_db()
    try:
        count = database.execute(
            'DELETE FROM jokes WHERE joke_id=?;',
            (joke_id,)
        ).rowcount
        database.commit()
        if count > 0:
            logging.info('Removed joke #%s', joke_id)
            result = True
        else:
            result = False
        return result
    except sqlite3.Error as err:
        logging.error('Unable to remove joke: %s', err)
        return False

def joke_random(category_id=0, joke_rank=None):
    """
    Returns a random joke ID.

    :param category_id: category ID
    :type category_id: int
    :param joke_rank: joke ranking
    :typ joke_rank: int
    """
    database = get_db()
    try:
        # execute database query
        if category_id > 0 and joke_rank:
            # limit to specific category and ranking
            jokes = database.execute(
                "SELECT * FROM jokes WHERE category_id=? AND joke_rank >= ?;",
                (category_id, joke_rank,)
            )
        elif category_id > 0:
            # limit to specific category
            jokes = database.execute(
                "SELECT * FROM jokes WHERE category_id=?;",
                (category_id,)
            )
        elif category_id == 0 and joke_rank:
            # all jokes but with specific ranking
            jokes = database.execute(
                "SELECT * FROM jokes WHERE joke_rank=?;",
                (joke_rank,)
            )
        else:
            # get _all_ the jokes
            jokes = database.execute("SELECT * FROM jokes;")
        # prepare result
        result = {}
        jokes = [dict(row) for row in jokes.fetchall()]
        random_joke = random.choice(jokes)
        result["results"] = [random_joke]
        ans = result
    except sqlite3.Error as err:
        logging.error('Unable to get jokes: %s', err)
        return False
    return ans



@BP.route("/<int:joke_id>", methods=["GET"])
def api_joke_get(joke_id):
    """
    This function shows a particular joke

    :param joke_id: joke ID
    :type joke_id: int
    """
    logging.info("Retrieve joke #%s", joke_id)
    return Response(
        json.dumps(joke_get(joke_id)),
        status=200,
        mimetype="application/json"
    )

@BP.route("", methods=["POST"])
def api_joke_create():
    """
    This function creates a new joke
    """
    # execute and return result
    result_data = json.loads(request.data)
    logging.info('Create joke %s', result_data["item"]["text"])
    result = joke_set(
        result_data["item"]["category_id"],
        result_data["item"]["text"],
        result_data["item"]["rank"]
    )
    return Response(
        return_result(result),
        status=200,
        mimetype="application/json"
    )

@BP.route("/<int:joke_id>", methods=["PUT", "POST"])
def api_joke_update(joke_id):
    """
    This function updates an existing joke

    :param joke_id: joke ID
    :type joke_id: int
    """
    # execute and return result
    logging.info('Update joke %s', joke_id)
    result_data = json.loads(request.data)
    result = joke_set(
        result_data["item"]["category_id"],
        result_data["item"]["text"],
        result_data["item"]["rank"],
        joke_id
    )
    return Response(
        return_result(result),
        status=200,
        mimetype="application/json"
    )

@BP.route("/<int:joke_id>", methods=["DELETE"])
def api_joke_delete(joke_id):
    """
    This function removes a joke

    :param joke_id: joke ID
    :type joke_id: int
    """
    logging.info('Delete joke %s', joke_id)
    result = joke_delete(joke_id)
    return Response(
        return_result(result),
        status=200,
        mimetype="application/json"
    )

@BP.route("/random", methods=["GET"])
def api_joke_random():
    """
    This function shows a random joke
    """
    # return a random joke
    result = joke_random()
    return Response(json.dumps(result), mimetype="application/result")

@BP.route("/random/<int:category_id>", methods=["GET"])
def api_joke_random_from_category(category_id):
    """
    This function shows a random joke from a particular category

    :param category_id: category ID
    :type category_id: int
    """
    # return a random joke
    result = joke_random(category_id=category_id)
    return Response(json.dumps(result), mimetype="application/result")

@BP.route("/random/<category_name>", methods=["GET"])
def api_joke_random_from_category_by_name(category_name):
    """
    This function shows a random joke from a particular category by name

    :param category_name: category name
    :type category_name: str
    """
    # return a random joke
    try:
        category = get_category_id_by_name(category_name)
        category_id = next(iter(category['results'][0].values()))
        result = joke_random(category_id=category_id)
        return Response(json.dumps(result), mimetype="application/result")
    except IndexError:
        logging.error('Category not found')
        return False

@BP.route("/random/<int:category_id>/<int:joke_rank>", methods=["GET"])
def api_joke_random_from_category_with_rank(category_id, joke_rank):
    """
    This function shows a random joke with ranking
    from a particular category

    :param category_id: category ID
    :type category_id: int
    :param joke_rank: joke ranking
    :type joke_rank: int
    """
    # return a random joke
    result = joke_random(category_id=category_id, joke_rank=joke_rank)
    return Response(json.dumps(result), mimetype="application/result")

@BP.route("/random/<category_name>/<int:joke_rank>", methods=["GET"])
def api_joke_random_from_category_with_rank_by_name(category_name, joke_rank):
    """
    This function shows a random joke with ranking
    from a particular category by name

    :param category_name: category name
    :type category_name: str
    :param joke_rank: joke ranking
    :type joke_rank: int
    """
    # return a random joke
    try:
        category = get_category_id_by_name(category_name)
        category_id = next(iter(category['results'][0].values()))
        result = joke_random(category_id=category_id, joke_rank=joke_rank)
        return Response(json.dumps(result), mimetype="application/result")
    except IndexError:
        logging.error('Category not found')
        return False
