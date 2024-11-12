#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
joke_api shared functions
"""
import json
import logging
import sqlite3

from .db import get_db

def return_result(result):
    """
    This function simply returns an operation's status in result

    :param result: boolean whether successful
    :type result: bool
    """
    ret = {}
    if result:
        ret = {
            "code": 0,
            "message": "SUCCESS"
        }
    else:
        ret = {
            "code": 1,
            "message": "FAILURE"
        }
    return json.dumps(ret)

def get_category_id_by_name(category_name):
    """
    Returns a category ID by name.

    :param category_name: category name
    :type category_name: str
    """
    database = get_db()

    try:
        categories = database.execute(
            "SELECT category_id FROM categories WHERE category_name=?;",
            (category_name,)
        )
        # return result
        return {"results": [dict(row) for row in categories.fetchall()]}
    except IndexError:
        logging.error('Category not found')
        return False
    except sqlite3.Error as err:
        logging.error('Unable to find category: %s', err)
        return False
