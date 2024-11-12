#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
joke_api /api/categories blueprint
"""
import json
import logging
import sqlite3

from flask import (
    Blueprint, Response, request
)

from .db import get_db
from .api_shared import return_result, get_category_id_by_name

BP = Blueprint('api_categories', __name__, url_prefix='/api/categories')

def category_get(category_id):
    """
    This function retrieves a category's information

    :param category_id: category ID
    :type category_id: int
    """
    database = get_db()
    try:
        if category_id > 0:
            # return one particular category
            categories = database.execute(
                "SELECT * FROM categories WHERE category_id=?;",
                (category_id,)
            )
        else:
            # return all categories
            categories = database.execute("SELECT * FROM categories;")

        # return result
        return {"results": [dict(row) for row in categories.fetchall()]}
    except sqlite3.Error as err:
        logging.error('Unable to get category: %s', err)
        return False

def category_set(category_name, category_id=None, category_newid=None):
    """
    This function creates/updates a category

    :param category_id: category ID
    :type category_id: int
    :param category_newid: new category ID
    :type category_newid: int
    :param category_name: category name
    :type category_name: str
    """
    database = get_db()
    try:
        if category_id:
            # update existing category
            database.execute(
                """UPDATE categories SET category_id=?, category_name=?
                WHERE category_id=?""",
                (category_newid, category_name, category_id,)
            )
            database.commit()
            logging.info('Updated category %s', category_name)
            result = True
        else:
            # create new category
            database.execute(
                'INSERT INTO categories (category_name) VALUES (?)',
                (category_name,)
            )
            database.commit()
            logging.info('Created category %s', category_name)
            result = True
        return result
    except sqlite3.Error as err:
        logging.error('Unable to create/update category: %s', err)
        return False

def category_delete(category_id):
    """
    Deletes a category.

    :param category_id: category ID
    :type category_id: int
    """
    database = get_db()
    try:
        count = database.execute(
            'DELETE FROM categories WHERE category_id=?;',
            (category_id,)
        ).rowcount
        database.commit()
        if count > 0:
            logging.info('Removed category #%s', category_id)
            result = True
        else:
            result = False
        return result
    except sqlite3.Error as err:
        logging.error('Unable to remove category: %s', err)
        return False



@BP.route("/<int:category_id>", methods=["GET"])
def api_category_get(category_id):
    """
    This function shows a particular category

    :param category_id: category ID
    :type category_id: int
    """
    logging.info("Retrieve category #%s", category_id)
    return Response(
        json.dumps(category_get(category_id)),
        status=200,
        mimetype="application/json"
    )

@BP.route("/<category_name>", methods=["GET"])
def api_category_get_by_name(category_name):
    """
    This function shows a particular category by name

    :param category_name: category name
    :type category_name: str
    """
    category = get_category_id_by_name(category_name)
    category_id = next(iter(category['results'][0].values()))
    return api_category_get(category_id)

@BP.route("", methods=["POST"])
def api_category_create():
    """
    This function creates a new category
    """
    # execute and return result
    result_data = json.loads(request.data)
    logging.info('Create category %s', result_data["item"]["name"])
    result = category_set(result_data["item"]["name"])
    return Response(
        return_result(result),
        status=200,
        mimetype="application/json"
    )

@BP.route("/<int:category_id>", methods=["PUT", "POST"])
def api_category_update(category_id):
    """
    This function updates an existing category

    :param category_id: category ID
    :type category_id: int
    """
    # execute and return result
    logging.info('Update category %s', category_id)
    result_data = json.loads(request.data)
    result = category_set(
        result_data["item"]["name"], category_id, result_data["item"]["id"],
    )
    return Response(
        return_result(result),
        status=200,
        mimetype="application/json"
    )

@BP.route("/<category_name>", methods=["PUT"])
def api_category_update_by_name(category_name):
    """
    This function updates an existing category by name

    :param category_id: category name
    :type category_id: str
    """
    category = get_category_id_by_name(category_name)
    category_id = next(iter(category['results'][0].values()))
    return api_category_update(category_id)

@BP.route("/<int:category_id>", methods=["DELETE"])
def api_category_delete(category_id):
    """
    This function removes a category

    :param category_id: category ID
    :type category_id: int
    """
    logging.info('Delete category %s', category_id)
    result = category_delete(category_id)
    return Response(
        return_result(result),
        status=200,
        mimetype="application/json"
    )

@BP.route("/<category_name>", methods=["DELETE"])
def api_category_delete_by_name(category_name):
    """
    This function removes a category by name

    :param category_name: category name
    :type category_name: str
    """
    try:
        category = get_category_id_by_name(category_name)
        category_id = next(iter(category['results'][0].values()))
        return api_category_delete(category_id)
    except IndexError:
        logging.error('Category not found')
        return False
