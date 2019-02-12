# -*- coding: utf-8 -*
import os

import cson


def test_create_queries_return_safe_config(client):
    """Post a config file to /queries.

       Verify if the new config file is safe (no query description).
    """
    testdir = os.path.dirname(os.path.realpath(__file__))

    res = client.post("/queries",
                      data=open(os.path.join(testdir, "cson/config.cson")))

    # request returns an HTTP 200
    assert res.status_code == 200

    # the response is a correct CSON file
    try:
        safe_config = cson.loads(res.data)
    except Exception as ex:
        assert False, "The response is not a correct CSON file (%s)" % str(ex)

    # each query has been replaced by its md5 checksum
    assert safe_config["settings"][0]["query"] == 'dbee8e5efef34bed71d5db632c3938b1'
    assert safe_config["others"]["dict"]["query"] == '120f098643762d0bfa38f2c9816dcc7b'
    assert safe_config["others"]["aggregate"]["query"] == 'e83dde3367d06bee18e9e6d123ea9fe1'


def test_create_queries_with_malformed_config_file(client):
    """Post a malformed config file to /queries.

       Verify if the reponse is a HTTP 400 Bad Request error.
    """
    testdir = os.path.dirname(os.path.realpath(__file__))

    res = client.post("/queries",
                      data=open(os.path.join(testdir, "cson/config_malformed.cson")))

    assert res.status_code == 400


def test_post_same_config_file_twice(client):
    """No error shall be raised
    """
    testdir = os.path.dirname(os.path.realpath(__file__))

    res_first = client.post("/queries",
                            data=open(os.path.join(testdir, "cson/config.cson")))

    # request returns an HTTP 200
    assert res_first.status_code == 200

    res_second = client.post("/queries",
                             data=open(os.path.join(testdir, "cson/config.cson")))

    # request returns an HTTP 200
    assert res_second.status_code == 200

    # the two new configuration file are the same
    assert res_first.data == res_second.data
