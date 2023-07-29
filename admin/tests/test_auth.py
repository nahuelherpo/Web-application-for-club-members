import unittest
from src.web import create_app

app = create_app()
app.testing = True


class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.endpoint = '/api/auth'

    def test_login_valid_credentials(self):
        # caso en donde la contraseña y el usuari son validos
        response = self.app.post(
            self.endpoint, json={"user": "28456851", "password": "hola"})
        self.assertTrue(type(response.data) is bytes)
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_password(self):
        # caso en donde la contraseña es invalida
        response = self.app.post(
            self.endpoint, json={"user": "28456851", "password": "notvalid"})
        self.assertTrue(type(response.data) is bytes)
        self.assertEqual(response.status_code, 401)

    def test_login_invalid_user(self):
        # caso en donde el usuario es invalido
        response = self.app.post(
            self.endpoint, json={"user": "pepe", "password": "hola"})
        self.assertTrue(type(response.data) is bytes)
        self.assertEqual(response.status_code, 401)

    def test_login_invalid_body(self):
        # caso en donde no se envian los parametros
        response = self.app.post(
            self.endpoint, json={})
        self.assertTrue(type(response.data) is bytes)
        self.assertEqual(response.status_code, 400)

    def test_login_invalid_http_method(self):
        # caso en donde el metodo https no es el esperado
        response = self.app.get(
            self.endpoint, json={"user": "28456851", "password": "hola"})
        self.assertEqual(response.status_code, 405)


if __name__ == '__main__':
    unittest.main()
