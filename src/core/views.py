# Create your views here.

from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic import TemplateView, DetailView
from core.models import Speaker, Talk

class HomepageView(TemplateView):
    template_name = 'index.html'

#class TalkDetailView(DetailView):
#    model = Talk
    
def talk_detail(request, talk_id):
    talk = get_object_or_404(Talk, id=talk_id)
    return direct_to_template(request, 'core/talk_detail.html', {
        'talk': talk,
        'videos': talk.media_set.filter(type='YT'),
        'slides': talk.media_set.filter(type='SL'),
    })

    
def speaker_detail(request, slug):
    speaker = get_object_or_404(Speaker, slug=slug)
    return direct_to_template(request, 'core/speaker_detail.html', {'speaker': speaker})

def talks(request):
    return direct_to_template(request, 'core/talks.html', {
        'morning_talks': Talk.objects.at_morning(),
        'afternoon_talks': Talk.objects.at_afternoon(),
    })
    