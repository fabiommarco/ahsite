from django.http import HttpResponse
from django.template import RequestContext, Template
from django.urls import reverse
from django.utils.translation import activate, get_language
from app.models import (GeneralConfig, Event, Partners, Products)
from django.conf import settings

def i18n_url(request):
    '''reverse to right url language'''
    if hasattr(request, 'current_app') and 'admin' in request.current_app:
        return {}
    current_language = get_language()
    redirect_to = ''
    if current_language != settings.LANGUAGE_CODE:
        activate(settings.LANGUAGE_CODE)
        resolver_match = request.resolver_match
        if resolver_match:
            redirect_to = reverse(resolver_match.url_name,
                                  args=resolver_match.args,
                                  kwargs=resolver_match.kwargs)
            activate(current_language)
    return {"redirect_to": redirect_to}

def load_info(request):
    '''add basic info into context'''
    extra_context = {}
    extra_context['general_info'] = GeneralConfig.objects.latest('id')
    extra_context['events_link'] = Event.translated_objects.all()
    extra_context['partners_link'] = Partners.translated_objects.all()
    extra_context['products_link'] = Products.translated_objects.all()
    return extra_context
