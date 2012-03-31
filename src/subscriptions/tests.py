# coding: latin-1

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.utils.translation import ugettext_lazy as _
from django.test import TestCase
from django.test.client import Client

class SubscriptionFormTest(TestCase):
    def test_new_subscription(self):
        response = self.client.get('/inscricao/')
        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'base.html')
        
    def test_blank_form(self):
        response = self.client.post('/inscricao/')
        self.assertFormError(response, 'form', 'name', 'This field is required.')
        self.assertFormError(response, 'form', None, _(u'Você precisa informar seu e-mail ou seu telefone.'))
        
    def test_email_and_phone_blank(self):
        response = self.client.post('/inscricao/', {'name': 'teste', 'cpf': '11111111111'})
        self.assertFormError(response, 'form', None, _(u'Você precisa informar seu e-mail ou seu telefone.'))
    
    def test_add_complete_form(self):
        response = self.client.post('/inscricao/', {'name': 'teste', 'cpf': '11111111111', 'email': 'teste@mail.com', 'phone_0': '11', 'phone_1': '55552222'})
        self.assertRedirects(response, '/inscricao/1/sucesso/')
        
    def test_add_no_email_form(self):
        response = self.client.post('/inscricao/', {'name': 'teste', 'cpf': '11111111111', 'phone_0': '11', 'phone_1': '55552222'})
        self.assertRedirects(response, '/inscricao/1/sucesso/')
        
    def test_add_no_phone_form(self):
        response = self.client.post('/inscricao/', {'name': 'teste', 'cpf': '11111111111', 'email': 'teste@mail.com'})
        self.assertRedirects(response, '/inscricao/1/sucesso/')
    
    def test_cpf_less_than_eleven(self):
        response = self.client.post('/inscricao/', {'cpf': '1'})
        self.assertFormError(response, 'form', 'cpf', _(u'O CPF deve ter 11 dígitos.'))
        
    def test_cpf_higher_than_eleven(self):
        response = self.client.post('/inscricao/', {'cpf': '1234567890123'})
        self.assertFormError(response, 'form', 'cpf', _(u'O CPF deve ter 11 dígitos.'))
        
    def test_invalid_character(self):
        response = self.client.post('/inscricao/', {'cpf': '1234567890A'})
        self.assertFormError(response, 'form', 'cpf', _(u'O CPF deve conter apenas números.'))
        
    def test_invalid_email_format(self):
        response = self.client.post('/inscricao/', {'email': 'teste.mail.com'})
        self.assertFormError(response, 'form', 'email', 'Enter a valid e-mail address.')
        
    def test_phone_higher_than_twenty_digits(self):
        response = self.client.post('/inscricao/', {'phone_0': '11', 'phone_1': '5555567848949844949'})
        self.assertFormError(response, 'form', 'phone', 'Ensure this value has at most 20 characters (it has 22).')
        
    def test_duplicated_cpf(self):
        response1 = self.client.post('/inscricao/', {'name': 'teste1', 'cpf': '11111111111', 'email': 'teste1@mail.com'})
        self.assertRedirects(response1, '/inscricao/1/sucesso/')
        response2 = self.client.post('/inscricao/', {'name': 'teste2', 'cpf': '11111111111', 'email': 'teste2@mail.com'})
        self.assertFormError(response2, 'form', 'cpf', _(u'CPF já inscrito.'))
        
    def test_duplicated_email(self):
        response1 = self.client.post('/inscricao/', {'name': 'teste1', 'cpf': '11111111111', 'email': 'teste@mail.com'})
        self.assertRedirects(response1, '/inscricao/1/sucesso/')
        response2 = self.client.post('/inscricao/', {'name': 'teste2', 'cpf': '22222222222', 'email': 'teste@mail.com'})
        self.assertFormError(response2, 'form', 'email', _(u'E-mail já inscrito.'))
        
    def test_blank_email_but_not_phone(self):
        response1 = self.client.post('/inscricao/', {'name': 'teste1', 'cpf': '11111111111', 'phone_0': '11', 'phone_1': '55552222'})
        self.assertRedirects(response1, '/inscricao/1/sucesso/')
        response2 = self.client.post('/inscricao/', {'name': 'teste2', 'cpf': '22222222222', 'phone_0': '11', 'phone_1': '55552222'})
        self.assertRedirects(response2, '/inscricao/2/sucesso/')
        
    def test_blank_phone_but_not_email(self):
        response1 = self.client.post('/inscricao/', {'name': 'teste1', 'cpf': '11111111111', 'email': 'teste@teste.com.br'})
        self.assertRedirects(response1, '/inscricao/1/sucesso/')
        response2 = self.client.post('/inscricao/', {'name': 'teste2', 'cpf': '22222222222', 'email': 'teste2@teste.com.br'})
        self.assertRedirects(response2, '/inscricao/2/sucesso/')

    def test_invalid_phone_number(self):
        response = self.client.post('/inscricao/', {'phone_0': '11', 'phone_1': ''})
        self.assertFormError(response, 'form', 'phone', u'Número inválido.')
        
    def test_invalid_ddd_number(self):
        response = self.client.post('/inscricao/', {'phone_0': '', 'phone_1': '55552222'})
        self.assertFormError(response, 'form', 'phone', u'DDD inválido.')