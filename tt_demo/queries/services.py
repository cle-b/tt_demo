# -*- coding: utf-8 -*
from flask import Response, abort
from flask import current_app as app

from .controllers import create_queries


def create_queries_from_cson(body):
    """Receive a CSON file that contains a list of queries.

    Record the queries in the database.

    Returns a safe CSON file where query descriptions have been replaced by keys.
    """
    try:
        safe_config = create_queries(body, app.mongo.db)
    except ValueError as ex:
        abort(400)  # TODO add message

    return Response(safe_config,
                    mimetype="application/cson; charset=utf-8",
                    headers={"Content-Disposition": "attachment;filename=safeconfig.cson"})
