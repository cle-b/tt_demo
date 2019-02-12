# -*- coding: utf-8 -*
import json

from flask import abort
import jinja2
import pymodm

from .controllers import execute_query_find, execute_query_aggregate
from ..queries.controllers import get_query_description


def query(id, body):

    # get the query description
    success, description = get_query_description(id)
    if not success:
        abort(404)

    # apply filter (even if the filter is empty of if the description is not a template) 
    new_description = jinja2.Template(description).render(body)

    # transform to json
    try:
        prepared_query = json.loads(new_description)
    except json.JSONDecodeError as ex:
        abort(400)

    # execute a search based on the find or aggregate function (its depends of the query)
    if isinstance(prepared_query, dict):
        results = execute_query_find(prepared_query)
    elif isinstance(prepared_query, list):
        results = execute_query_aggregate(prepared_query)
    else:
        abort(400)

    # return a list of documents (can be empty)
    return results
