from django.http import HttpResponse
from django.template import RequestContext, Template
from django.urls import reverse
from django.utils.translation import activate, get_language
from django.conf import settings

def i18n_url(request):
    current_language = get_language()
    redirect_to = ''
    if current_language != settings.LANGUAGE_CODE:
        activate(settings.LANGUAGE_CODE)
        resolver_match = request.resolver_match
        redirect_to = reverse(resolver_match.url_name,
                              args=resolver_match.args,
                              kwargs=resolver_match.kwargs)
        activate(current_language)
    return {"redirect_to": redirect_to}
