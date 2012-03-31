# coding: latin-1

from django import forms
from django.core.validators import EMPTY_VALUES
from django.utils.translation import ugettext_lazy as _
from subscriptions.validators import CpfValidator
from subscriptions.models import Subscription

class PhoneWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widget = (
            forms.TextInput(attrs={'size':'2', 'maxlength':'2'}),
            forms.TextInput(attrs={'size':'15', 'maxlength':'9'}))
        super(PhoneWidget, self).__init__(widget, attrs)
        
    def decompress(self, value):
        if not value:
            return [None, None]
        
        return value.split('-')
        
class PhoneField(forms.MultiValueField):
    widget = PhoneWidget
    
    def __init__(self, *args, **kwargs):
        fields = (
            forms.IntegerField(),
            forms.IntegerField())
        super(PhoneField, self).__init__(fields, *args, **kwargs)
        
    def compress(self, data_list):
        if not data_list:
            return None
        
        if data_list[0] in EMPTY_VALUES:
            raise forms.ValidationError(u'DDD inválido.')
            
        if data_list[1] in EMPTY_VALUES:
            raise forms.ValidationError(u'Número inválido.')
        
        return '%s-%s' % tuple(data_list)


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        exclude = ('created_at', 'paid',)
    
    # sobrescrever os atributos abaixo do Model para aplicação da validators
    # e tornar e-mail opcional em caso de preenchimento do telefone
    cpf = forms.CharField(label=_('CPF'), validators=[CpfValidator])
    email = forms.EmailField(label=_('E-mail'), required=False)
    phone = PhoneField(label=_('Telefone'), required=False)

    # metodos iniciados com _ sao considerados "privados" por convencao
    def _unique_check(self, fieldname, error_message):
        '''
        Metodo para verificar a unicidade de campos no cadastro
        para evitar duplicidade. Utilizado no momento para
        verificar CPF e e-mail.
        '''
        
        # dicionario com os campos do formulario ja validados e tratados (cleaned_data).
        # exemplo: { 'email': self.cleaned_data['email'] }
        param = { fieldname: self.cleaned_data[fieldname] }
        try:
            # Acesso ao manager para recuperar os objetos que satisfacam o filtro
            # Caso encontre um ou mais objetos, lanca uma excecao 
            s = Subscription.objects.get(**param)
        except Subscription.DoesNotExist:
            return self.cleaned_data[fieldname]
        raise forms.ValidationError(error_message)
        
    def clean_cpf(self):
        return self._unique_check('cpf', _(u'CPF já inscrito.'))

    def clean_email(self):
        return self._unique_check('email', _(u'E-mail já inscrito.'))
    
    def clean(self):
        '''
        Metodo para validar se o campo email ou o campo phone do formulario esta preenchido.
        Chamado apos os cleans dos fields.
        '''
        super(SubscriptionForm, self).clean()
        
        if not self.cleaned_data.get('email') and not self.cleaned_data.get('phone'):
            raise forms.ValidationError(_(u'Você precisa informar seu e-mail ou seu telefone.'))
            
        return self.cleaned_data

