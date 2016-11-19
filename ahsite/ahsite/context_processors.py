from django.http import HttpResponse
from django.template import RequestContext, Template
from django.urls import reverse
from django.utils.translation import activate, get_language

def i18n_url(request):
    current_language = get_language()
    activate('pt')
    resolver_match = request.resolver_match
    redirect_to = reverse(resolver_match.url_name,
                          args=resolver_match.args,
                          kwargs=resolver_match.kwargs)
    activate(current_language)
    return {"redirect_to": redirect_to}
