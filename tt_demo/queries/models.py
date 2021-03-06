# -*- coding: utf-8 -*
import json
import hashlib

from pymodm import fields, MongoModel


class Query(MongoModel):
    """Model for the query

    The document look like this

    { "_id": id, "description": "{\"the\":{\"query\":\"description\"}}"} 

        where id is the checksum of description
    """
    id = fields.CharField(primary_key=True)
    description = fields.CharField(required=True)

    def __init__(self, description=None):
        # using the checksum as key in order to avoid at least two problems:
        #       * key collision
        #       * query duplication
        # Tip: we can know the id of a query document without requesting the database
        desc = json.dumps(description, ensure_ascii=False)
        checksum = hashlib.md5(desc.encode("utf-8")).hexdigest()
        super(Query, self).__init__(id=checksum,
                                    description=desc)
