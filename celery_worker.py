import config
from celery_utils import init_celery, celery
from src import create_app

app = create_app(config.DevelopmentConfig)
init_celery(celery, app)
