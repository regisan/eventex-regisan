# coding: latin-1

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

def CpfValidator(value):
    if not value.isdigit():
        raise ValidationError(_(u'O CPF deve conter apenas números.'))
    if len(value) != 11:
        raise ValidationError(_(u'O CPF deve ter 11 dígitos.'))
    if not digito_valido(value):
        raise ValidationError(_(u'CPF inválido.'))
        
def digito_valido(cpf):
    num = cpf[:-2]
    digito = cpf[-2:]
    pesos = range(2,11)
    pesos.reverse()
    
    list_numbers = []

    for n in num:
        list_numbers.append(int(n))
        
    i = 10
    soma = 0
    for lst in list_numbers:
        soma += lst * i
        i -= 1
        
    quoc = soma / 11
    mod = soma % 11
    
    dig1 = 0
    if (mod >= 2):
        dig1 = 11 - mod
    
    list_numbers.append(dig1)
    pesos = range(2,12)
    pesos.reverse()
    
    i = 11
    soma = 0
    for lst in list_numbers:
        soma += lst * i
        i -= 1
        
    quoc = soma / 11
    mod = soma % 11
    
    dig2 = 0
    if (mod >= 2):
        dig2 = 11 - mod
    
    if (str(dig1) + str(dig2)) == digito:
        return True
    
    return False
 