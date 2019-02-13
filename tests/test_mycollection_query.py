# -*- coding: utf-8 -*


def test_query_one_document_without_filter(client):
    #   query:
    #     domain: "test_domain_2"
    #     my_key: "2017"
    res = client.post("/mycoll/query?id=ef9a570053038ba08b5ca89dac4a3a6c",
                      json={})

    # request returns an HTTP 200
    assert res.status_code == 200

    # there is only one document
    documents = res.json
    assert len(documents) == 1

    # the document is the expected one
    assert documents[0]["domain"] == "test_domain_2"
    assert documents[0]["my_key"] == "2017"


def test_query_one_document_with_filter(client):
    #   query:
    #     domain: "test_domain_2"
    #     my_key: "{{filter}}"

    res = client.post("/mycoll/query?id=61dbb89ca5de54506143f3a7a07c2763",
                      json={"filter": "2018"})

    # request returns an HTTP 200
    assert res.status_code == 200

    # there is only one document
    documents = res.json
    assert len(documents) == 1

    # the document is the expected one
    assert documents[0]["domain"] == "test_domain_2"
    assert documents[0]["my_key"] == "2018"


def test_query_two_documents_with_filter(client):
    #   query:
    #     domain: "test_domain_2"
    #     my_key: "{{filter}}"
    res = client.post("/mycoll/query?id=61dbb89ca5de54506143f3a7a07c2763",
                      json={"filter": "2020"})

    # request returns an HTTP 200
    assert res.status_code == 200

    # there are two documents
    documents = res.json
    assert len(documents) == 2

    # the document is the expected one
    for document in documents:
        assert document["domain"] == "test_domain_2"
        assert document["my_key"] == "2020"


def test_query_empty_document_with_filter(client):
    #   query:
    #     domain: "test_domain_2"
    #     my_key: "{{filter}}"
    res = client.post("/mycoll/query?id=61dbb89ca5de54506143f3a7a07c2763",
                      json={"filter": "2021"})

    # request returns an HTTP 200
    assert res.status_code == 200

    # there is only no document
    documents = res.json
    assert len(documents) == 0


def test_query_aggregate(client):
    # query:[  
    #     $match:
    #       domain:"test_domain_2"
    #     ,  
    #     $group:
    #       _id: "$my_key"
    #       my_key: 
    #           $sum: 1

    res = client.post("/mycoll/query?id=89da2cbd2e566a77b0e96ebf06c26daf",
                      json={})

    # request returns an HTTP 200
    assert res.status_code == 200

    # there are 4 documents
    documents = res.json
    assert len(documents) == 4


def test_query_unknown_id(client):
    #   query:
    #     domain: "test_domain_2"
    #     my_key: "{{filter}}"

    res = client.post("/mycoll/query?id=66af44ae18e586",
                      json={})

    # request returns an HTTP 404
    assert res.status_code == 404
