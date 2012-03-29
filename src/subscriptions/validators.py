# coding: latin-1

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

def CpfValidator(value):
    if not value.isdigit():
        raise ValidationError(_(u'O CPF deve conter apenas n�meros.'))
    if len(value) != 11:
        raise ValidationError(_(u'O CPF deve ter 11 d�gitos.'))