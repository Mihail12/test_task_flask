from http import HTTPStatus

from flask_restx import Resource, Namespace

__all__ = (
    'webhook_ns', 'WebhookCreateAPI', 'WebhookUpdateDeleteAPI',
)

from src.marshal import airport_post, webhook_model
from src.tasks.airports import create_airport_task, update_airport_task, delete_airport_task

webhook_ns = Namespace('webhooks', description='Webhooks namespace')


class WebhookCreateAPI(Resource):
    """Resource/routes for create airport in task"""

    @webhook_ns.expect(airport_post, validate=True)
    @webhook_ns.marshal_with(webhook_model, envelope='resource')
    def post(self):
        create_airport_task.delay(webhook_ns.payload)
        return HTTPStatus.CREATED


class WebhookUpdateDeleteAPI(Resource):
    """Resource/routes for update and delete airport in task"""

    @webhook_ns.expect(airport_post, validate=True)
    @webhook_ns.marshal_with(webhook_model, envelope='resource')
    def put(self, sid):
        update_airport_task.delay(webhook_ns.payload, sid)
        return HTTPStatus.OK

    @webhook_ns.marshal_with(webhook_model, envelope='resource')
    def delete(self, sid):
        delete_airport_task.delay(sid)
        return HTTPStatus.NO_CONTENT
