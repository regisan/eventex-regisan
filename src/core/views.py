# Create your views here.

from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404
from core.models import Speaker, Talk

def speaker_detail(request, slug):
    speaker = get_object_or_404(Speaker, slug=slug)
    return direct_to_template(request, 'core/speaker_detail.html', {'speaker': speaker})

def talks(request):
    return direct_to_template(request, 'core/talks.html', {
        'morning_talks': Talk.objects.at_morning(),
        'afternoon_talks': Talk.objects.at_afternoon(),
    })
