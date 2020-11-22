import csv
from http import HTTPStatus

from flask_restx import Resource, Namespace
from sqlalchemy import exc

from src.marshal import airport_get_put, airport_upload_parser, airport_post, airport_file_upload
from src.models import Airport, db, get_object_or_404


__all__ = (
    'airport_ns', 'AirportUploadAPI', 'AirportUpdateRetrieveAPI', 'AirportListAddAPI',
)


airport_ns = Namespace('airports', description='Airports namespace')


@airport_ns.response(code=HTTPStatus.CREATED, description=HTTPStatus.CREATED.description)
@airport_ns.response(code=HTTPStatus.BAD_REQUEST, description=HTTPStatus.BAD_REQUEST.description)
class AirportUploadAPI(Resource):
    """Resource/routes for csv file uploading endpoints"""

    @airport_ns.expect(airport_upload_parser, validate=True)
    @airport_ns.marshal_with(airport_file_upload, envelope='resource')
    def post(self, *args, **kwargs):
        data = airport_upload_parser.parse_args()
        field_names = data['file'].readline().decode().lower().strip().split(',')
        reader = csv.DictReader(
            data['file'].read().decode().splitlines(),
            skipinitialspace=True,
            fieldnames=field_names,
        )
        objects = []
        for row in reader:
            if data['insert_with_ids'] == 'false':
                del row['id']
            objects.append(
                Airport.from_upload(row),
            )
        try:
            db.session.bulk_save_objects(objects)
            db.session.commit()
            result = HTTPStatus.CREATED
        except exc.IntegrityError:
            db.session.rollback()
            result = {'result': 'Error while inserting'}, HTTPStatus.BAD_REQUEST
        return result


@airport_ns.response(code=HTTPStatus.OK, description=HTTPStatus.OK.description)
@airport_ns.response(code=HTTPStatus.NOT_FOUND, description=HTTPStatus.NOT_FOUND.description)
class AirportUpdateRetrieveAPI(Resource):
    """Resource/routes for get, update and delete airport endpoints"""

    @airport_ns.marshal_with(airport_get_put, envelope='resource')
    def get(self, sid):
        """External facing airport endpoint GET

        Gets an existing Airport object by id

        Args:
            sid (int): id of airport object

        Returns:
            json: serialized airport object

        """
        airport = get_object_or_404(Airport.query.only_not_deleted(), sid)
        return airport

    @airport_ns.expect(airport_post, validate=True)
    @airport_ns.marshal_with(airport_get_put, envelope='resource')
    def put(self, sid):
        """External facing airport endpoint PUT

        Gets an existing Airport object by id and update it

        Args:
            sid (int): id of airport object

        Returns:
            json: serialized airport object

        """
        return Airport.update(airport_ns.payload, sid)

    @airport_ns.response(code=HTTPStatus.NO_CONTENT, description=HTTPStatus.NO_CONTENT.description)
    def delete(self, sid):
        Airport.delete(sid)
        return {'result': 'ok'}, HTTPStatus.NO_CONTENT


class AirportListAddAPI(Resource):
    """Resource/routes for add and list airport endpoints"""

    @airport_ns.response(code=HTTPStatus.CREATED, description=HTTPStatus.CREATED.description)
    @airport_ns.expect(airport_post, validate=True)
    @airport_ns.marshal_with(airport_get_put, envelope='resource')
    def post(self):
        return Airport.create(airport_ns.payload), HTTPStatus.CREATED

    @airport_ns.response(code=HTTPStatus.OK, description=HTTPStatus.OK.description)
    @airport_ns.marshal_with(airport_get_put, as_list=True)
    def get(self):
        return Airport.query.only_not_deleted().all()

