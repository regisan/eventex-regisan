# coding: latin-1

from django.db import models

# Create your models here.
class Subscription(models.Model):
    name = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name
        
    class Meta:
        ordering = ["created_at"]
        verbose_name = u"Inscri��o"
        verbose_name_plural = u"Inscri��es"