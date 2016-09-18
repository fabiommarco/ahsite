# -*- coding: utf-8 -*-
"""
    AH Website - LFMarques - 2016
    luizfelipe.unesp@gmail.com
"""
import functools
import json

from app.models import *
from app.forms import ContactForm, ApplyJobForm, NewsletterForm

from collections import MutableMapping
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage


def load_basic_info(method):
    '''general_info
        add a global variable in globals() named general_info
    '''
    @functools.wraps(method)
    def wrapper(request, *args, **kwargs):
        g = method.func_globals
        g['general_info'] = GeneralConfig.objects.latest('id')
        g['events_link'] = Event.objects.all()
        g['partners_link'] = Partners.objects.all()

        res = method(request,*args, **kwargs)
        return res
    return wrapper

@load_basic_info
def home(request):
    latest_feeds = News.objects.order_by('-news_date')[:5]
    return render(request, 'index.html', 
                  {'is_index':True,
                   'products':Products.objects.all(),
                   'general_info':general_info,
                   'events_link':events_link,
                   'partners_link':partners_link,
                   'news':latest_feeds})

@load_basic_info
def about_company(request,r=None):
    about = AboutCompany.objects.latest('id')
    return render(request, 'about_company.html', 
                  {'about':about,
                   'general_info':general_info,
                   'events_link':events_link,
                   'partners_link':partners_link,})

@load_basic_info
def agricutural_prices(request):
    prices = AgriculturalFiles.objects.order_by('-ap_date')[:5]
    return render(request, 'agricutural_prices.html', 
                  {'prices':prices,
                   'general_info':general_info,
                   'events_link':events_link,
                   'partners_link':partners_link,})

@load_basic_info
def event_view(request, event_slug=None):
    return render(request, 'event_view.html',
                  {'event':get_object_or_404(Event, event_slug=event_slug),
                   'general_info':general_info,
                   'events_link':events_link,
                   'partners_link':partners_link,})

@load_basic_info
def partners_view(request, partner_slug=None):
    return render(request, 'partners_view.html',
                  {'partner':get_object_or_404(Partners, partner_slug=partner_slug),
                    'general_info':general_info,
                    'events_link':events_link,
                    'partners_link':partners_link,})

@load_basic_info
def news(request):
    all_news = News.objects.filter()
    paginator = Paginator(all_news, 6)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        all_news = paginator.page(all_news)
    except (EmptyPage, InvalidPage):
        all_news = paginator.page(paginator.num_pages)

    return render(request, 'news.html', {'all_news':all_news,
                                         'general_info':general_info,
                                         'events_link':events_link,
                                         'partners_link':partners_link,})

@load_basic_info
def news_view(request, news_slug=None):
    return render(request, 'news_view.html',
                  {'news':get_object_or_404(News, news_slug=news_slug),
                   'general_info':general_info,
                   'events_link':events_link,
                   'partners_link':partners_link,})

@load_basic_info
def sales(request):
    return render(request, 'sales.html',
                  {'sale':Sale.objects.latest("id"),
                   'general_info':general_info,
                   'events_link':events_link,
                   'partners_link':partners_link,
                   'url_contact':reverse('new_contact', args=['sale'])})
@load_basic_info
def magazine(request):

    magazines = Magazine.objects.order_by('-magazine_date')[:5]

    magazine = {}
    if magazines:
        magazine = magazines[0]
    return render(request, 'magazine.html',
                  {'magazine': magazine,
                   'old_versions': magazines[1:],
                   'general_info':general_info,
                   'events_link':events_link,
                   'partners_link':partners_link})


@load_basic_info
def products_list(request):
    return render(request, 'products_list.html',
                 {'products':Products.objects.all(),
                  'general_info':general_info,
                  'events_link':events_link,
                  'partners_link':partners_link})

@load_basic_info
def product_view(request, product_slug=None):
    return render(request, 'product_view.html',
                  {'product':get_object_or_404(Products, product_slug=product_slug),
                   'general_info':general_info,
                   'events_link':events_link,
                   'partners_link':partners_link,})


@load_basic_info
def talk_with_us(request):
    return render(request, 'talk-with-us.html', 
                  {'url_contact':reverse('new_contact', args=['contact']),
                   'general_info':general_info,
                   'events_link':events_link,
                   'partners_link':partners_link})

@load_basic_info
def work_with_us(request):
    return render(request, 'work-with-us.html',
                  {'jobs':Jobs.objects.filter(),
                   'is_apply_job':True,
                   'url_contact':reverse('new_contact', args=['contact']),
                   'general_info':general_info,
                   'events_link':events_link,
                   'partners_link':partners_link,})

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

        if contact_type == 'contact' or contact_type == 'sale':
            contact_form = ContactForm(request.POST)
        elif contact_type == 'apply_job':
            contact_form = ApplyJobForm(request.POST, request.FILES)
            apply_job_context = True
        else:
            return_data = {'success': False}

        if not contact_form.is_valid():
            return_data = {'success': False, 'errors' : [(k, v[0]) for k, v in contact_form.errors.items()]}
            messages.add_message(request, messages.ERROR, 
                                 'Parece que algo de errado aconteceu. Por favor, tente novamente mais tarde!')
        else:
            if contact_type == 'sale':
                extra_recipient = Sale.objects.latest('id')
                contact_form.send(request, extra_recipient.sale_email)
            else:
                contact_form.send(request)
            messages.add_message(request, messages.SUCCESS, 'Obrigado! Sua mensagem foi enviada.')
        if apply_job_context:
            # return render(request, 'work-with-us.html', {})
            return HttpResponseRedirect(reverse('work_with_us', args=()))
        return HttpResponse(json.dumps(return_data, ensure_ascii=False))

    return HttpResponseRedirect("/")


@csrf_exempt
def new_newsletter(request):
    if request.method == "POST":
        newsletter_form = NewsletterForm(request.POST)
        data = {'success': True}
        if not newsletter_form.is_valid():
            data = {
                'success': False,
                'errors': [(k, v[0]) for k, v in newsletter_form.errors.items()]
            }
        else:
            newsletter_form.save()
        return HttpResponse(json.dumps(data, ensure_ascii=False))
    return HttpResponseRedirect("/")


def list_newsletter(request):
    return render(request,
                  'admin/newsletter/list_newsletter.html',
                  {'newsletter':Newsletter.objects.filter()})

def handler404(request):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response
