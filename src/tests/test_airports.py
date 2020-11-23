from io import BytesIO

from src.models import Airport
from .base import BaseTests


class AirportsTestCase(BaseTests):
    @classmethod
    def setUpClass(cls):
        super(AirportsTestCase, cls).setUpClass()
        cls.test_data = {
            "name": "string",
            "city": "string",
            "country": "string",
            "iata": "string",
            "icao": "string",
            "latitude": "string",
            "longitude": "string",
            "altitude": "string",
            "timezone": "string",
            "dst": "string",
            "tz": "string",
            "type": "string",
            "source": "string",
        }

    def test_create_airport(self):
        response = self.client.post('/api/airports/', json=self.test_data)
        self.assertEqual(response.status_code, 201)
        response_json = response.json['resource']
        airport = Airport.query.get(response_json['id'])
        self.assertEqual(airport.name, response_json['name'])

    # @patch('f_app.celery_app.send_task', return_value=Mock(id='fibonacci_id'))
    def test_get_airports(self):
        response = self.client.get('/api/airports/')
        self.assertEqual(response.status_code, 200)
        airports = Airport.query.all()
        self.assertEqual(len(response.json), len(airports))

    def test_get_one_airport_object(self):
        response = self.client.get(f'/api/airports/{self.airport1.id}')
        self.assertEqual(response.status_code, 200)
        response_json = response.json['resource']
        self.assertEqual(response_json['name'], self.airport1.name)

    def test_get_404_airport_object(self):
        response = self.client.get(f'/api/airports/{9999}')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(list(response.json.keys()), ['message'])

    def test_put_one_airport_object(self):
        response = self.client.put(f'/api/airports/{self.airport1.id}', json=self.test_data)
        self.assertEqual(response.status_code, 200)
        response_json = response.json['resource']
        airport = Airport.query.get(response_json['id'])
        self.assertEqual(self.test_data['name'], airport.name)

    def test_put404_airport_object(self):
        response = self.client.put(f'/api/airports/{9999}', json=self.test_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(list(response.json.keys()), ['message'])

    def test_delete_one_airport_object(self):
        airport1_id = self.airport1.id
        self.assertFalse(self.airport1.is_deleted)
        response = self.client.delete(f'/api/airports/{self.airport1.id}')
        self.assertEqual(response.status_code, 204)
        airport = Airport.query.get(airport1_id)
        self.assertTrue(airport.is_deleted)

        response = self.client.get(f'/api/airports/{airport1_id}')
        self.assertEqual(response.status_code, 404)

    def test_delete_not_existed_airport_object(self):
        response = self.client.delete(f'/api/airports/{9999}')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(list(response.json.keys()), ['message'])

    def test_upload_csv_file(self):
        data = {
            'file': (BytesIO(b'FILE CONTENT'), 'test.csv')
        }
        response = self.client.post('/api/airports/upload-csv/', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        response_json = response.json['resource']
        self.assertEqual(response_json['result'], "File has been uploaded.")
