# coding: latin-1

import datetime
from django.conf.urls.defaults import patterns, url
from django.http import HttpResponse
from django.contrib import admin
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext
from subscriptions.models import Subscription

class SubscriptionAdmin(admin.ModelAdmin):
    '''
    Classe que representa o módulo de administração da app Subscriptions
    '''
    
    # lista de colunas a serem exibidas
    list_display = ('name', 'email', 'phone', 'created_at', 'subscribed_today', 'paid')
    # atributo de ordenação
    date_hierarchy = 'created_at'
    # lista de campos utilizados na busca
    search_fields = ('name', 'cpf', 'email', 'phone', 'created_at')
    # list_filter = ['created_at']
    # lista de atributos do filtro
    list_filter = ('paid',)
    # custom actions
    actions = ['mark_as_paid']
    
    def subscribed_today(self, obj):
        '''
        Método para indicar se a inscrição foi realizada neste dia 
        '''
        return obj.created_at.date() == datetime.date.today()
    
    subscribed_today.short_description = u'Inscrito hoje?'
    subscribed_today.boolean = True
    
    def mark_as_paid(self, request, queryset):
        '''
        Custom action para marcar inscrições como pagas
        '''
        count = queryset.update(paid=True)
        
        msg = ungettext(
            u'%(count)d inscrição foi marcada como paga.',
            u'%(count)d inscrições foram marcadas como pagas',
            count
        ) % {'count': count}
        self.message_user(request, msg)
        
    mark_as_paid.short_description = _(u'Marcar como pagas')
    
    def export_subscriptions(self, request):
        '''
        View para exportar inscritos em arquivo formato csv
        '''
        subscriptions = self.model.objects.all()
        
        # list comprehension para contenar nome com email, separados por (,)
        rows = [','.join([s.name, (s.email or s.phone)]) for s in subscriptions] 
        
        # prepara o response com mimetype
        response = HttpResponse('\r\n'.join(rows))
        response.mimetype = 'text/csv'
        response['Content-Disposition'] = 'attachment; filename=inscricoes.csv'
        
        return response
        
    def get_urls(self):
        '''
        Método sobrescrito de ModelAdmin para responder pela url exportar-inscricoes
        '''
        original_urls = super(SubscriptionAdmin, self).get_urls()
        extra_url = patterns('',
            # Decoramos a view com a admin_view
            url(r'exportar-inscricoes/$',
                self.admin_site.admin_view(self.export_subscriptions),
                name='export_subscriptions')
            )
            # urls do admin sao muito permissivas e aceitam varios matches
            # a url da app deve ter precedencia
        return extra_url + original_urls
    
admin.site.register(Subscription, SubscriptionAdmin)
