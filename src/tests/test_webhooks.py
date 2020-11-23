from unittest.mock import patch

from src.tests.base import BaseTests


class WebhooksTestCase(BaseTests):
    @classmethod
    def setUpClass(cls):
        super(WebhooksTestCase, cls).setUpClass()
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

    @patch('src.resources.webhooks.create_airport_task.delay')
    def test_create_airport_async_task(self, _):
        response = self.client.post('/api/webhooks/start-task/create/', json=self.test_data)
        self.assertEqual(response.status_code, 200)
        response_json = response.json['resource']
        self.assertEqual(list(response_json.keys()), ['result'])

    @patch('src.resources.webhooks.update_airport_task.delay')
    def test_update_airport_async_task(self, _):
        response = self.client.put(f'/api/webhooks/start-task/{self.airport1.id}/', json=self.test_data)
        self.assertEqual(response.status_code, 200)
        response_json = response.json['resource']
        self.assertEqual(list(response_json.keys()), ['result'])

    @patch('src.resources.webhooks.delete_airport_task.delay')
    def test_delete_airport_async_task(self, _):
        response = self.client.delete(f'/api/webhooks/start-task/{self.airport1.id}/')
        self.assertEqual(response.status_code, 200)
        response_json = response.json['resource']
        self.assertEqual(list(response_json.keys()), ['result'])
