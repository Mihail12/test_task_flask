import logging
import os

logger = logging.getLogger(__name__)


class DevelopmentConfig(object):
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))

    db_engine = os.environ.get("SQL_ENGINE", 'sqlite3')
    db_user = os.environ.get("SQL_USER", 'user')
    db_password = os.environ.get("SQL_PASSWORD", 'password')
    db_host = os.environ.get("SQL_HOST", 'localhost')
    db_port = os.environ.get("SQL_PORT", '')
    db_name = os.environ.get("SQL_DATABASE", 'db.sqlite3')
    db_type = os.environ.get("DATABASE", 'sqlite')

    mq_user = os.environ.get("RABBITMQ_DEFAULT_USER", 'rabbitmq')
    mq_password = os.environ.get("RABBITMQ_DEFAULT_USER", 'rabbitmq')
    mq_host = os.environ.get("RABBITMQ_HOST", 'rabbit')

    SQLALCHEMY_DATABASE_URI = f'{db_type}+{db_engine}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    CELERY_BROKER_URL = f'amqp://{mq_user}:{mq_password}@{mq_host}:5672/'
    CELERY_RESULT_BACKEND = f'amqp://{mq_user}:{mq_password}@{mq_host}:5672/'

    SECRET_KEY = "test"
    ENCRYPTION_KEY = "test"

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # service code used for data blocking
    DATA_BLOCKING_CODE = "FTRS Data Blocking"
