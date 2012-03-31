# coding: latin-1

from django.db import models

# Create your models here.
class Subscription(models.Model):
    name = models.CharField('Nome', max_length=100)
    cpf = models.CharField('CPF', max_length=11, unique=True)
    email = models.EmailField('E-mail', unique=True, blank=False, null=True)
    phone = models.CharField('Telefone', max_length=20, blank=False, null=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    paid = models.BooleanField()
    
    def __unicode__(self):
        return self.name
        
    class Meta:
        ordering = ["created_at"]
        verbose_name = u"Inscrição"
        verbose_name_plural = u"Inscrições"