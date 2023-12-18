from flask import Blueprint
from flask_restx import Api

bp_api  = Blueprint(
    name="api",
    import_name=__name__,
    url_prefix="/api/v1"
)

authorizations = {
    "apikey": {
        "type": "apiKey",
        "in": "header",
        "name": "X-API-KEY"
    }
}

api     = Api(
    app=bp_api,
    version="1.0",
    title="RESTx API",
    description="Flask-RESTx Example",
    doc="/docs",
    encoding="UTF-8",
    authorizations=authorizations
)

from my_app.api.v1.auth import auth_namespace
from my_app.api.v1.post import post_namespace

api.add_namespace(ns=auth_namespace, path="/auth")
api.add_namespace(ns=post_namespace, path="/post")