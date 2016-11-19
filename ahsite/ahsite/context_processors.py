from django.http import HttpResponse
from django.template import RequestContext, Template
from django.urls import reverse
from django.utils.translation import activate, get_language
from app.models import (GeneralConfig,Event,Partners,Products)

def i18n_url(request):
    current_language = get_language()
    activate('pt')
    resolver_match = request.resolver_match
    redirect_to = reverse(resolver_match.url_name,
                          args=resolver_match.args,
                          kwargs=resolver_match.kwargs)
    activate(current_language)
    return {"redirect_to": redirect_to}

def load_info(request):
    extra_context = {}
    extra_context['general_info'] = GeneralConfig.objects.latest('id')
    extra_context['events_link'] = Event.objects.all()
    extra_context['partners_link'] = Partners.objects.all()
    extra_context['products_link'] = Products.objects.all()
    return extra_context