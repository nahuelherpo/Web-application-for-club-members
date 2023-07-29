import unittest
from src.web import create_app
import json

app = create_app()
app.testing = True

class PaymentTestCase(unittest.TestCase):
    """ Clase de testing del endpoint /api/me/payments """

    def setUp(self):
        """ Método de inicialización de la clase """
        
        self.client = app.test_client()
        self.valid_jwt = self.client.post("/api/auth", json={"user": "28456851", "password": "hola"}).get_data(as_text=True).strip('\n').strip('"') 
        self.image =  "data:image/jpeg;base64,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"
        self.invalid_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NjYxMTkzMiwianRpIjoiYmE3YjUzZjUtN2U3NS00NmU3LThjNzMtMTA3YzE1OThjZGQ5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Ii0yIiwibmJmIjoxNjg2NjExOTMyLCJjc3JmIjoiNTE3YjEwYzMtYTc0OC00OTI3LTkwZjUtNzlhZjliYjJiZGU4IiwiZXhwIjoxNjg2Njk4MzMyfQ.T_m-p4B8GhXE49bOpHZR-k27C1otctxZK5h9zb8PKZE"
    
    def test_get_pagos_200(self):
        
        response = self.client.get("/api/me/payments", headers={"Authorization": f"Bearer {self.valid_jwt}"},
          content_type= "application/json")
        self.assertEqual(response.status_code, 200)
        

    def test_get_pagos_401(self):

        response = self.client.get("/api/me/payments", headers={"Authorization": f"Bearer {self.invalid_jwt}"},
          content_type= "application/json",)
        self.assertEqual(response.status_code, 401)


    def test_registrar_pago_200(self):
        
        response = self.client.post("/api/me/payments", headers={"Authorization": f"Bearer {self.valid_jwt}"},
          content_type= "application/json", json = {
            "paid_by": "Pagado por el asociado.",
            "payment_date": "12/02/2022",
            "fee_id": 3,
            "amount_paid": 100,
            "image": str(self.image) })
    
        self.assertEqual(response.status_code, 200)

    def test_registrar_pago_401(self):
        
        response = self.client.post("/api/me/payments", headers={"Authorization": f"Bearer {self.invalid_jwt}"},
          content_type= "application/json", json = {
            "paid_by": "Pagado por el asociado 1.",
            "payment_date": "12/02/2022",
            "fee_id": 2,
            "amount_paid": 100,
            "image": f"{self.image}" })
        self.assertEqual(response.status_code, 401)

    def test_registrar_pago_422(self):
        
        response = self.client.post("/api/me/payments", headers={"Authorization": f"Bearer {self.valid_jwt}"},
          content_type= "application/json", json = {
            "paid_by": "Pagado por el asociado 1.",
            "payment_date": "12/02/2022",
            "fee_id": 2,
            "amount_paid": 100,
            "image": f"{self.image}" })

        self.assertEqual(response.status_code, 422)


    def test_registrar_pago_500(self):
        
        response = self.client.post("/api/me/payments", headers={"Authorization": f"Bearer {self.valid_jwt}"},
          content_type= "application/json", json = {
            "paid_by": "Pagado por el asociado 1.",
            "payment_date": "12/02/2022",
            "fee_id": 4,
            "amount_paid": 100,
            "image": "unaimagencualquiera" })

        self.assertEqual(response.status_code, 500)
