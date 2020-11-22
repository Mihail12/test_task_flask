"""API route declarations

Imports any Flask resources and registers them as API routes to accept
requests and return responses on the Flask server.
"""
from flask import Blueprint
from flask_restx import Api

from src.marshal import marshal_models
from src.resources import airport_ns, webhook_ns


def register_routes(_app):
    """Registers api resources/routes with Flask app

    Args:
        _app (object): Flask app object

    """
    from src import resources

    api_blueprint = Blueprint("api", __name__)
    api = Api(api_blueprint, catch_all_404s=False)
    api.add_namespace(airport_ns)

    airport_ns.add_resource(
        resources.AirportUpdateRetrieveAPI, "/<int:sid>/", strict_slashes=False)
    airport_ns.add_resource(
        resources.AirportListAddAPI, "/", strict_slashes=False)
    airport_ns.add_resource(
        resources.AirportUploadAPI, "/upload-csv/", strict_slashes=False)

    api.add_namespace(marshal_models)

    api.add_namespace(webhook_ns)
    webhook_ns.add_resource(
        resources.WebhookCreateAPI, "/start-task/create/", strict_slashes=False)
    webhook_ns.add_resource(
        resources.WebhookUpdateDeleteAPI, "/start-task/<int:sid>/", strict_slashes=False)

    _app.register_blueprint(api_blueprint, url_prefix="/api")
