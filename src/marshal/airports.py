import werkzeug
from flask_restx import fields, Namespace, reqparse

airport_models = Namespace('Airports-models', description='Airports namespace')

airport_get_put = airport_models.model('Airport-GET-PUT', {
    'id': fields.String,
    'name': fields.String(required=True),
    'city': fields.String,
    'country': fields.String,
    'iata': fields.String,
    'icao': fields.String,
    'latitude': fields.String,
    'longitude': fields.String,
    'altitude': fields.String,
    'timezone': fields.String,
    'dst': fields.String,
    'tz': fields.String,
    'type': fields.String,
    'source': fields.String,
})


airport_post = airport_models.model('Airport-POST', {
    'id': fields.String,
    'name': fields.String(required=True),
    'city': fields.String(required=True),
    'country': fields.String(required=True),
    'iata': fields.String,
    'icao': fields.String,
    'latitude': fields.String,
    'longitude': fields.String,
    'altitude': fields.String,
    'timezone': fields.String,
    'dst': fields.String,
    'tz': fields.String,
    'type': fields.String(required=True),
    'source': fields.String(required=True),
})


airport_upload_parser = reqparse.RequestParser()
airport_upload_parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files', required=True)
airport_upload_parser.add_argument('insert_with_ids', type=str)