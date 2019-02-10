# -*- coding: utf-8 -*
import io
import os

import cson


def test_create_queries_return_safe_config(client):
    """Post a config file to /queries.

       Verify if the new config file is safe (no query description).
    """

    testdir = os.path.dirname(os.path.realpath(__file__))

    res = client.post("/queries",
                      data=open(os.path.join(testdir, "cson/config.cson")))

    assert res.status_code == 200

    try:
        safe_config = cson.loads(res.data)
    except Exception as ex:
        assert False, str(ex)

    assert isinstance(safe_config["settings"][0]["query"], str)


def test_create_queries_with_malformed_config_file(client):
    """Post a malformed config file to /queries.

       Verify if the reponse is a HTTP 400 Bad Request error.
    """
    testdir = os.path.dirname(os.path.realpath(__file__))

    res = client.post("/queries",
                      data=open(os.path.join(testdir, "cson/config_malformed.cson")))

    assert res.status_code == 400
