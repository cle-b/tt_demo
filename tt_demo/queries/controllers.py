# -*- coding: utf-8 -*
import json
import hashlib

import cson

from .models import Query


def search_and_replace_queries(config):
    """Search and replace all query descriptions by a key (its checksum) in the
       configuration dictionary. It's a generator, only a query is replaced at each
       call.

    Args:
        config: A configuration dictionary with query descriptions.

    Returns:
        A Query object (as an generator).
    """
    for k, v in config.items():
        if k == "query":
            new_query = Query(v)
            config[k] = new_query.name
            yield new_query
        elif isinstance(v, dict):
            for result in search_and_replace_queries(v):
                yield result
        elif isinstance(v, list):
            for d in v:
                if isinstance(d, dict):
                    for result in search_and_replace_queries(d):
                        yield result


def create_queries(cson_content):
    """Create the queries from the CSON configuration file

    Args:
        cson_content: The CSON configuration file content.

    Returns:
        The CSON configuration file content with key instead of description for the queries.

    Raises:
        ValueError: The CSON if malformed.
    """
    try:
        config = cson.loads(cson_content)
    except Exception as ex:  # no specific exception seems to be raised in case of malformed CSON
        raise ValueError("An error occured during the CSON parsing: {0}".format(ex))

    queries = list(search_and_replace_queries(config))  # walks through config recursively

    # create or update all the queries using a bulk command for better performance.
    # bulk_write with update is not available with pymodm (for insert or update)
    # Therefore, we first retreive all existing query name in order to bulk_create
    # only the new ones.
    query_names = get_all_query_names()
    new_queries = []
    new_query_names = []
    for query in queries:
        if (query.name not in query_names) and (query.name not in new_query_names):
            new_queries.append(query)
            new_query_names.append(query.name)
    if len(new_queries) > 0:
        Query.objects.bulk_create([new_query for new_query in new_queries])

    return cson.dumps(config, indent=True, ensure_ascii=False)


def get_all_query_names():
    """Returns an array with all query IDs"""
    return [query.name for query in list(Query.objects.only("name"))]


def get_query_description(query_id):
    """Get the description of the query query_id.

    Returns the query description has a string.
    """
    try:
        query = Query.objects.get({'_id': query_id})
        return True, query.description
    except Query.DoesNotExist:
        return False, "This query does not exist"
