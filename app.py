"""Main Flask application entrypoint

Example::
    $ python app.py

"""
import config
from celery_utils import celery
from src import create_app

app = create_app(config.DevelopmentConfig, celery=celery)


@app.shell_context_processor
def make_shell_context():
    """Adds imports to default shell context for easier use"""
    from src.models import Airport, db

    return {
        "Airport": Airport,
        "db": db,
    }
