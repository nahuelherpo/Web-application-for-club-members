import unittest
from src.web import create_app
import json
from src.core import disciplines

app = create_app()
app.testing = True


class DisciplinesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.disciplines_endpoint = '/api/club/disciplines'
        self.my_disciplines_endpoint = '/api/me/disciplines'
        self.auth_endpoint = '/api/auth'

    def test_disciplines_list(self):

        # Make the GET request from endpoint
        response = self.app.get(self.disciplines_endpoint)
        self.assertTrue(type(response.data) is bytes)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Check if the response is correct (compare the content with the seeds)
        expected_data = "[{'categories': [{'days': 'Miercoles y Jueves', 'hour_fence': '9 a 11', 'instructors': 'Marcos', 'name': 'Mini'}, {'days': 'Viernes y Sábados', 'hour_fence': '13 a 15', 'instructors': 'Patricia', 'name': 'Juvenil'}], 'monthly_price': 450.0, 'name': 'Básquet'}]"

        data = str(response.get_json())

        self.assertEqual(data, expected_data)

    def test_unauthorized_my_disciplines_list(self):

        # Make the GET request from endpoint
        response = self.app.get(self.my_disciplines_endpoint)
        self.assertTrue(type(response.data) is bytes)

        # Check if the response was successful
        self.assertEqual(response.status_code, 401)

    def test_authorized_my_disciplines_list(self):
        # A mock user from seeds
        response = self.app.post(self.auth_endpoint, json={"user": "28456851", "password": "hola"})
        self.assertTrue(type(response.data) is bytes)
        self.assertEqual(response.status_code, 200)

        # Make the GET request from endpoint
        response = self.app.get(self.my_disciplines_endpoint)
        self.assertTrue(type(response.data) is bytes)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Check if the response is correct (compare the content with the seeds)
        expected_data = "[]"

        data = str(response.get_json())

        self.assertEqual(data, expected_data)

if __name__ == '__main__':
    unittest.main()
