# -*- coding: utf-8 -*

import json
import hashlib

import cson
from pymongo import UpdateOne


def search_and_replace_queries(config):
    """Search and replace all query descriptions by a key (its checksum) in the
       configuration dictionary.

        When a query description is found, we:
            * stringify it
            * calculate its checksum
            * replace the description by its checksum
            * return the pair (checksum, str_description)

    Args:
        config: A configuration dictionary with query descriptions.

    Returns:
        The pair (checksum, str_description)
    """
    for k, v in config.items():
        if k == "query":
            str_description = json.dumps(v, ensure_ascii=False)
            checksum = hashlib.md5(str_description.encode("utf-8")).hexdigest()
            config[k] = checksum
            yield (checksum, str_description)
        elif isinstance(v, dict):
            for result in search_and_replace_queries(v):
                yield result
        elif isinstance(v, list):
            for d in v:
                if isinstance(d, dict):
                    for result in search_and_replace_queries(d):
                        yield result


def create_queries(cson_content, db):
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

    # insert all the queries using a bulk command for better performance.
    # insert a query only if not exists
    # using the checksum as key in order to avoid at least two problems:
    #       * key collision
    #       * query duplication
    # in case of performance issue, change document like this
    # {"name": checksum, "description": str_description} and an index for "name"
    db.myqueries.bulk_write([UpdateOne({checksum: {"$exists": True}},
                                       {"$set": {checksum: str_description}},
                                       upsert=True) for (checksum, str_description) in queries])

    return cson.dumps(config, indent=True, ensure_ascii=False)
