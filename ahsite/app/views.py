# -*- coding: utf-8 -*-
"""
    AH Website - LFMarques - 2016
    luizfelipe.unesp@gmail.com
"""
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from app.forms import ContactForm,ApplyJobForm
from app.models import *
import functools
import json
from collections import MutableMapping

def load_basic_info(method):
    '''general_info
        add a global variable in globals() named general_info
    '''
    @functools.wraps(method)
    def wrapper(request, *args, **kwargs):
        g = method.func_globals
        g['general_info'] = GeneralConfig.objects.latest('id')
        res = method(request,*args, **kwargs)
        return res
    return wrapper

@load_basic_info
def home(request):
    return render(request, 'index.html', {'is_index':True, 'general_info':general_info})

@load_basic_info
def about_company(request,r=None):
    about = AboutCompany.objects.latest('id')
    return render(request, 'about_company.html', {'about':about,'general_info':general_info})

def agricutural_prices(request):
    prices = AgriculturalFiles.objects.order_by('-ap_date')[:5]
    return render(request, 'agricutural_prices.html', {'prices':prices,})

def events(request):
    all_events = Event.objects.filter()
    paginator = Paginator(all_events, 6)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        all_events = paginator.page(all_events)
    except (EmptyPage, InvalidPage):
        all_events = paginator.page(paginator.num_pages)

    return render(request, 'events.html', {'all_events':all_events})


def event_view(request, event_slug=None):
    return render(request, 'event_view.html', 
                 {'event':get_object_or_404(Event, event_slug = event_slug)})


def news(request):
    all_news = News.objects.filter()
    paginator = Paginator(all_news, 6)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        all_news = paginator.page(all_news)
    except (EmptyPage, InvalidPage):
        all_news = paginator.page(paginator.num_pages)

    return render(request, 'news.html', {'all_news':all_news})


def news_view(request, news_slug=None):
    return render(request, 'news_view.html', 
                 {'news':get_object_or_404(News, news_slug = news_slug)})

    
def sales(request):
    return render(request, 'sales.html', 
                 {'sale':Sale.objects.latest("id"),
                  'url_contact':reverse('new_contact', args=['sale'])})

def talk_with_us(request):
    context = {'url_contact':reverse('new_contact', args=['contact'])}
    return render(request, 'talk-with-us.html', context)

def work_with_us(request):
    context = {'url_contact':reverse('new_contact', args=['apply_job'])}
    jobs = Jobs.objects.filter()
    context.update({'jobs':jobs,'is_apply_job':True})

    return render(request, 'work-with-us.html', context)

@csrf_exempt
def new_contact(request,contact_type):
    '''
        send contact email
        :params:
            contact_type: str - contact (to user email contact) or apply_job (user sending CV)
    '''
    if request.method == "POST":
        return_data = {'success': True}
        apply_job_context = False

        if contact_type == 'contact' or contact_type == 'sale' :
            contactForm = ContactForm(request.POST)
        elif contact_type == 'apply_job':
            contactForm = ApplyJobForm(request.POST, request.FILES)
            apply_job_context = True
        else:
            return_data = {'success': False}

        if not contactForm.is_valid():
            return_data = {'success': False, 'errors' : [(k, v[0]) for k, v in contactForm.errors.items()] }
            messages.add_message(request, messages.ERROR, 'Parece que algo de errado aconteceu. Por favor, tente novamente mais tarde!')
        else:
            if contact_type == 'sale':
                extra_recipient = Sale.objects.latest('id')
                contactForm.send(request, extra_recipient.sale_email)
            else:
                contactForm.send(request)
            messages.add_message(request, messages.SUCCESS, 'Obrigado! Sua mensagem foi enviada.')
        if apply_job_context:
            # return render(request, 'work-with-us.html', {})
            return HttpResponseRedirect(reverse('work_with_us', args=()))
        return HttpResponse(json.dumps(return_data, ensure_ascii=False)) #, content_type='application/json; charset=UTF-8'

    return HttpResponseRedirect("/")