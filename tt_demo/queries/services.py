# -*- coding: utf-8 -*
from flask import Response, abort

from .controllers import create_queries, get_all_query_ids, get_query_description


def create_queries_from_cson(body):
    """Receive a CSON file that contains a list of queries.

    Record the queries in the database.

    Returns a safe CSON file where query descriptions have been replaced by keys.
    """
    try:
        safe_config = create_queries(body)
    except ValueError as ex:
        abort(400)  # TODO add message

    return Response(safe_config,
                    mimetype="application/cson; charset=utf-8",
                    headers={"Content-Disposition": "attachment;filename=safeconfig.cson"})


def list_queries():
    """Returns an array with the ID of all the queries already recorded in the database.
    """
    return get_all_query_ids()


def get_query(query_id):
    exists, description = get_query_description(query_id)
    # TODO add 404 in openapi.yaml
    if not exists:
        abort(404)

    return {"id": query_id, 
            "description": description}
