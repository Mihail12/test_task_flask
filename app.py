"""Main Flask application entrypoint

Example::
    $ python att.py

"""
import config
from src import create_app

app = create_app(config.DevelopmentConfig)


@app.shell_context_processor
def make_shell_context():
    """Adds imports to default shell context for easier use"""
    from src.models import Airport, db

    return {
        "Airport": Airport,
        "db": db,
    }
