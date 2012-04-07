"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse
from models import Speaker, Contact, Talk, Course


class HomepageUrlTest(TestCase):
    def test_success_when_get_homepage(self):
        """
        Tests the index homepage.
        """
        response = self.client.get(reverse('core:homepage'))
        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'index.html')

class SpeakerTest(TestCase):
    def test_create_speaker(self):
        s = Speaker(name = 'Bob Marley',
                    slug = 'bob-marley',
                    url = 'http://bobmarley.com')
        s.save()
        ce = Contact(kind='E', value='bobmarley@reggae.jm')
        cf = Contact(kind='F', value='11-5555-9999')
        cp = Contact(kind='P', value='11-5555-8888')
        s.contact_set.add(ce)
        s.contact_set.add(cf)
        s.contact_set.add(cp)
        self.assertQuerysetEqual(s.contact_set.all().order_by(), 
                                ['<Contact: E, bobmarley@reggae.jm>',
                                '<Contact: F, 11-5555-9999>',
                                '<Contact: P, 11-5555-8888>'])
                                
    def test_add_talk_to_speaker(self):
        s = Speaker(name = 'Jimi Hendrix',
                    slug = 'jimi-hendrix',
                    url = 'http://jimi.hendrix.com')
        s.save()
        t = Talk(title = 'First Talk',
                 start_time = '15:00')
        t.save()
        
        s.talk_set.add(t)
        self.assertQuerysetEqual(s.talk_set.all(), 
                                ['<Talk: First Talk>'])
        self.assertQuerysetEqual(t.speakers.all(), 
                                ['<Speaker: Jimi Hendrix>'])
        
class TalkTest(TestCase):
    def test_create_talk(self):
        t = Talk(title = 'First Talk',
                 start_time = '15:00')
        t.save()
        self.assertQuerysetEqual(Talk.objects.all(), 
                                ['<Talk: First Talk>'])
  

class CourseTest(TestCase):
    def test_create_course(self):
        c = Course(title = 'Some Course',
                   start_time='09:00',
                   slots=20)
        c.save()
        self.assertQuerysetEqual(Course.objects.all(),
                                ['<Course: Some Course>'])
        