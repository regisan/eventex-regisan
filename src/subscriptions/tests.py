"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SubscriptionFormTest(TestCase):
    def test_new_subscription(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        response = self.client.get('/inscricao')
        self.assertEquals(301, response.status_code)
        #self.assertTemplateUsed(response, 'new.html')
