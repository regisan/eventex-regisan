# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, resolve
from django.shortcuts import get_object_or_404
from forms import SubscriptionForm
from models import Subscription

def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)

def new(request):
    form = SubscriptionForm()
    context = RequestContext(request, {'form': form})
    return render_to_response('subscriptions/new.html', context)
    
def create(request):
    form = SubscriptionForm(request.POST)
    
    if not form.is_valid():
        context = RequestContext(request, {'form': form})
        return render_to_response('subscriptions/new.html', context)
    
    subscription = form.save()
    return HttpResponseRedirect(reverse('subscriptions:success', args=[subscription.pk]))
    
def success(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)
    context = RequestContext(request, {'subscription': subscription})
    return render_to_response('subscriptions/success.html', context)