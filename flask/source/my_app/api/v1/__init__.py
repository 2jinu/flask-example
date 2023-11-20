from flask import Blueprint
from flask_restx import Api

from my_app.api.v1.auth import auth_namespace

bp_api = Blueprint(
    name="api",
    import_name=__name__,
    url_prefix="/api/v1"
)
api = Api(
    app=bp_api,
    version="1.0",
    title="RESTX API",
    description="flask-restx Example",
    doc="/docs",
    encoding="UTF-8"
)

api.add_namespace(ns=auth_namespace, path="/auth")