from django.conf.urls.defaults import patterns, url
from views import HomepageView, TalkDetailView, TalkListView

urlpatterns = patterns('core.views',
    url(r'^$', HomepageView.as_view(), name='homepage'),
    url(r'^palestras/$', TalkListView.as_view(), name='talks'),
    url(r'^palestras/(\d+)/$', 'talk_detail', name='talk_detail'),
    url(r'^palestrante/([-\w]+)/$', 'speaker_detail', name='speaker_detail'),
)
