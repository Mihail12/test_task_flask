import logging
import os

logger = logging.getLogger(__name__)


class DevelopmentConfig(object):
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/airports'

    HOST = "localhost"
    PORT = "5000"
    SECRET_KEY = "test"
    ENCRYPTION_KEY = "test"

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # service code used for data blocking
    DATA_BLOCKING_CODE = "FTRS Data Blocking"
