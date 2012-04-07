from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf.urls.defaults import patterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'src.views.home', name='home'),
    # url(r'^src/', include('src.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^inscricao/', include('subscriptions.urls', namespace='subscriptions')),
    (r'^', include('core.urls', namespace='core')),
)

urlpatterns += staticfiles_urlpatterns()