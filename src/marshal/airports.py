import werkzeug
from flask_restx import fields, Namespace, reqparse


marshal_models = Namespace('Airports-models', description='Airports namespace')

airport_file_upload = marshal_models.model('Airport-file-upload', {
    'result': fields.String(default='File has been uploaded.'),
})


airport_get_put = marshal_models.model('Airport-GET-PUT', {
    'id': fields.Integer,
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


airport_post = marshal_models.model('Airport-POST', {
    'id': fields.Integer(readonly=True),
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
airport_upload_parser.add_argument('insert_with_ids', type=str,
                                   help='set to "false" if you want export file without "ids" in it')


webhook_model = marshal_models.model('Webhook', {
    'result': fields.String(default='task has been started'),
})
