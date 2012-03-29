# coding: latin-1

from django import forms
from django.utils.translation import ugettext_lazy as _
from subscriptions.validators import CpfValidator
from subscriptions.models import Subscription

class SubscriptionForm(forms.Form):
    name = forms.CharField(label=_('Nome'), max_length=100)
    cpf = forms.CharField(label=_('CPF'), validators=[CpfValidator])
    email = forms.EmailField(label=_('E-mail'), required=False)
    phone = forms.CharField(label=_('Telefone'), required=False, max_length=20)

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
        #if not self.cleaned_data['email'] == '':
        return self._unique_check('email', _(u'E-mail já inscrito.'))
    
    def clean(self):
        '''
        Metodo para validar se o campo email ou o campo phone do formulario esta preenchido.
        Chamado apos os cleans dos fields.
        '''
        if not self.cleaned_data.get('email') and not self.cleaned_data.get('phone'):
            raise forms.ValidationError(_(u'Você precisa informar seu e-mail ou seu telefone.'))
            
        return self.cleaned_data
    
    def save(self):
        '''
        Metodo para salvar os dados do form, pois este form nao herda de ModelForm.
        '''
        s = Subscription()
        s.name = self.cleaned_data['name']
        s.cpf = self.cleaned_data['cpf']
        s.email = self.cleaned_data['email']
        s.phone = self.cleaned_data['phone']
        s.save()
        return s
    
    
    #class Meta:
    #    model = Subscription
    #    exclude = ('created_at', 'paid',)