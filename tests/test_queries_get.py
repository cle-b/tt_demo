# -*- coding: utf-8 -*
import time

from tt_demo.queries.models import Query


def test_get_query(client):
    """Get an ID and a description
    """
    # create a new query and save it in the db
    new_query = Query({"mynewquery": time.time()})
    new_query.save()

    # get the new query
    res = client.get("/query/%s" % new_query.id)

    # request returns an HTTP 200
    assert res.status_code == 200

    # the query description is correct
    assert new_query.id == res.json["id"]
    assert new_query.description == res.json["description"]


def test_get_query_not_exists(client):
    """Get a HTTP 404 error
    """
    # try to retrieve a query that not exists
    res = client.get("/query/%s" % (str(time.time())))

    # request returns an HTTP 404
    assert res.status_code == 404
