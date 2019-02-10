# -*- coding: utf-8 -*
import os

import connexion
from flask_pymongo import PyMongo


def create_app(app_name, mongodb_uri, port=9090, debug=False):    
    options = {"swagger_ui": debug}

    specification_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "openapi/")

    app = connexion.FlaskApp(app_name,
                             port=port,
                             specification_dir=specification_dir,
                             options=options,
                             debug=debug)  # fix as FLASK_DEBUG flag not works...

    app.add_api('swagger-ttdemo.yaml')

    app.app.config["MONGO_URI"] = mongodb_uri
    app.app.mongo = PyMongo(app.app)

    return app


if __name__ == '__main__':
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    mongdb_uri = os.getenv("TT_MONGO_URI", "mongodb://localhost:27017/mytest")

    app = create_app(__name__,
                     mongodb_uri=mongdb_uri,
                     debug=debug)
    app.run()
