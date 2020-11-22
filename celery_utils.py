import os

from celery import Celery


def init_celery(celery, app):
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask


def make_celery(app_name=__name__):
    mq_user = os.environ.get("RABBITMQ_DEFAULT_USER", 'rabbitmq')
    mq_password = os.environ.get("RABBITMQ_DEFAULT_USER", 'rabbitmq')
    mq_host = os.environ.get("RABBITMQ_HOST", 'rabbit')
    mq_uri = f'amqp://{mq_user}:{mq_password}@{mq_host}:5672/'
    return Celery(app_name, backend=mq_uri, broker=mq_uri)


celery = make_celery()
