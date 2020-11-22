from celery_utils import celery
from src.models import Airport


@celery.task
def create_airport_task(data):
    """Task that creates Airport entry"""
    Airport.create(data)
    return 'created'


@celery.task
def update_airport_task(data, sid):
    """Task that updates Airport entry by sid"""
    Airport.update(data, sid)
    return 'updated'


@celery.task
def delete_airport_task(sid):
    """Task that deletes Airport entry by sid"""
    Airport.delete(sid)
    return 'deleted'
