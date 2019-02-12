# -*- coding: utf-8 -*
import pymodm


def execute_query_find(query):
    """Search document in mycoll collection using a query.

    Returns a list of documents.
    """
    documents = []
    for document in list(pymodm.connection._get_db().mycoll.find(query)):
        document.pop("_id")
        documents.append(document)
    return documents


def execute_query_aggregate(query):
    """Search document in mycoll collection using a query.

    Returns a list of documents.
    """
    documents = []
    for document in list(pymodm.connection._get_db().mycoll.aggregate(query)):
        document.pop("_id")
        documents.append(document)
    return documents
