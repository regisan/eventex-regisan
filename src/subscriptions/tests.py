"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

class SubscriptionFormTest(TestCase):
    def test_new_subscription(self):
        c = Client()
        response = c.get('/inscricao/')
        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'base.html')
        
    def test_add_subscription(self):
        response = self.client.post('/inscricao/', {'name': 'teste', 'cpf': '11111111111', 'email': 'teste@mail.com', 'phone': '11-5555-2222'})
        self.assertRedirects(response, '/inscricao/1/sucesso/')
    
    def test_invalid_subscription(self):
        response = self.client.post('/inscricao/')
        self.assertIsNotNone(response.context['messages'])
    