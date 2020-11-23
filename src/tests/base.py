import os
import unittest

from src.models import Airport, db

from app import app

TEST_DB = 'test.db'


class BaseTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['BASEDIR'] = os.getcwd()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                                os.path.join(app.config['BASEDIR'], TEST_DB)
        self.client = app.test_client()
        db.drop_all()
        db.create_all()
        self.airport1 = Airport(**{
            "name": "name1",
            "city": "city",
            "country": "country",
            "iata": "iata",
            "tz": "tz",
            "type": "type",
            "source": "source",
        })
        self.airport2 = Airport(**{
            "name": "name2",
            "city": "city1",
            "country": "country",
            "iata": "iata",
            "tz": "tz3",
            "type": "type",
            "source": "source",
        })
        db.session.add(self.airport1)
        db.session.add(self.airport2)
        db.session.commit()

        self.handle = 'test'

    # executed after each test
    def tearDown(self):
        db.session.close()

    @classmethod
    def tearDownClass(cls):
        os.remove(os.path.join(app.config['BASEDIR'], TEST_DB))
