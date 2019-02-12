# -*- coding: utf-8 -*
import time

from tt_demo.queries.models import Query


def test_list_queries(client):
    """List shall return all available queries.
    """
    # create a new query
    new_query = Query({"mynewquery": time.time()})

    # retrieve the list of all available queries
    res = client.get("/queries")

    # request returns an HTTP 200
    assert res.status_code == 200

    # the query is not available
    assert new_query.id not in res.json

    # save the query in the database
    new_query.save()

    # retrieve the list of all available queries
    res = client.get("/queries")

    # request returns an HTTP 200
    assert res.status_code == 200

    # the query is  available
    assert new_query.id in res.json


def test_list_queries_return_list(client):
    """List shall return a list.
    """
    # retrieve the list of all available queries
    res = client.get("/queries")

    # request returns an HTTP 200
    assert res.status_code == 200

    # the return data is a list
    assert isinstance(res.json, list)
