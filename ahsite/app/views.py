# -*- coding: utf-8 -*-
"""
    AH Website -
    LFMarques - 2016
      luizfelipe.unesp@gmail.com

    Victor Cinaglia - 2016
      victorcinaglia@gmail.com

"""
import functools
import random
import json

from app.models import *
from app.forms import ContactForm, ApplyJobForm, NewsletterForm
from app.utils import reload_sys

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.conf import settings
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _


colors = [
    "c8d6b9",
    "faf3dd",
    "9dbad5",
    "769ecb",
    "f6cacb",
    "d99294",
    "d4cfbd",
    "e1cec9",
    "b4bad4",
    "d2c1ce",
    "dfd8dc",
    "ebe6e5",
    "70A1D7",
    "A1DE93",
    "F7F48B",
    "F47C7C",
    "FFF9AA",
    "FFD5B8",
    "FFB9B3",
    "ACECD5",
]
def get_or_redirect(model, language, view_name, **kwargs):
    object = get_object_or_404(model, **kwargs)
    # Custom handling if object's language does not match current langugage.
    if object.language != language:
        # Object has a parent, therefore it is a translation.
        if object.parent:
            if object.parent.language == language:
                # Parent's object language is the current language. Simply
                # retun the parent object itself.
                translated = object.parent
            else:
                # Parent's object is not the current language. Find an object
                # whose parent is the same as its own parent.
                translated = get_object_or_404(model.translated_objects,
                                               parent=object.parent)
        else:
            # Object does not have a parent, therefore it *is* a parent.
            # Find a translation whose parent is this object.
            translated = get_object_or_404(model.translated_objects,
                                           parent=object)
        kwargs = {k: getattr(translated, k) for k in kwargs.keys()}
        return redirect(reverse(view_name, kwargs=kwargs))
    return object

def home(request):
    '''return homepage'''
    latest_feeds = News.translated_objects.order_by('-news_date')[:4]
    farms = Farm.objects.all()

    for farm in farms:
        farm.initials = "".join([item[0] for item in farm.farm_name.split(" ")[0:2]])
        farm.color = random.choice(colors)

    return render(request, 'index.html',
                  {'is_index':True,
                   'products':Products.translated_objects.all(),
                   'news':latest_feeds,
                   "farms": farms})

def about_company(request):
    '''return about us'''
    about = AboutCompany.translated_objects.latest('id')
    return render(request, 'about_company.html',
                  {'about':about})

def agricutural_prices(request):
    '''return agricultural prices page'''
    prices = AgriculturalFiles.objects.order_by('-ap_date')[:5]
    return render(request, 'agricutural_prices.html',
                  {'prices':prices})

def environmental_responsability(request):
    '''return env resp page'''
    environmental = EnvironmentalResponsability.translated_objects.latest('id')
    return render(request, 'environmental.html',
                  {'environmental':environmental})

def event_view(request, event_slug=None):
    '''return event details page'''
    event = get_or_redirect(Event, language=request.LANGUAGE_CODE,
                              view_name='event_view',
                              event_slug=event_slug)
    if not isinstance(event, Event):
        return event
    return render(request, 'event_view.html',
                  {'event':event})

def partners_view(request, partner_slug=None):
    '''return partners view page'''
    partner = get_or_redirect(Partners, language=request.LANGUAGE_CODE,
                              view_name='partners_view',
                              partner_slug=partner_slug)
    if not isinstance(partner, Partners):
        return partner
    return render(request, 'partners_view.html',
                  {'partner':partner})

def news(request):
    '''return lastest news'''
    all_news = News.translated_objects.order_by('-news_date')
    paginator = Paginator(all_news, 6)

    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1

    try:
        all_news = paginator.page(page)
    except (EmptyPage, InvalidPage):
        all_news = paginator.page(paginator.num_pages)

    return render(request, 'news.html', {'all_news':all_news,
                                         'current_page':page})

def news_view(request, news_slug=None):
    '''return news details'''
    return render(request, 'news_view.html',
                  {'news':get_object_or_404(News, news_slug=news_slug)})

def sales(request):
    '''return sales page'''
    return render(request, 'sales.html',
                  {'sale':Sale.translated_objects.latest("id"),
                   'url_contact':reverse('new_contact', args=['sale'])})

def magazine(request):
    '''return latests magazines'''
    magazines = Magazine.objects.order_by('-magazine_date')[:5]

    magazine = {}
    if magazines:
        magazine = magazines[0]
    return render(request, 'magazine.html',
                  {'magazine': magazine,
                   'old_versions': magazines[1:]})

def product_view(request, product_slug=None):
    '''return products details page'''
    product = get_or_redirect(Products, language=request.LANGUAGE_CODE,
                              view_name='product_view',
                              product_slug=product_slug)
    if not isinstance(product, Products):
        return product
    choices = settings.BANNER_IMG.get(product.product_category)
    rand_img = random.choice(choices or random.randrange(1, 11))
    return render(request, 'product_view.html',
                  {'product': product, 'random_img': rand_img})

def talk_with_us(request):
    '''return contact page'''
    return render(request, 'talk-with-us.html',
                  {'url_contact':reverse('new_contact', args=['contact'])})

def work_with_us(request):
    '''return careers page'''
    return render(request, 'work-with-us.html',
                  {'jobs':Jobs.objects.filter(),
                   'is_apply_job':True,
                   'url_contact':reverse('new_contact', args=['apply_job'])})

@csrf_exempt
def new_contact(request, contact_type):
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
                                 _('Parece que algo de errado aconteceu. Por favor, tente novamente mais tarde!'))
        else:
            if contact_type == 'sale':
                extra_recipient = Sale.translated_objects.latest('id')
                contact_form.send(request, extra_recipient.sale_email)
            else:
                contact_form.send(request)
            messages.add_message(request, messages.SUCCESS, _('Obrigado! Sua mensagem foi enviada.'))
        if apply_job_context:
            return HttpResponseRedirect(reverse('work_with_us', args=()))
        return HttpResponse(json.dumps(return_data, ensure_ascii=False))

    return HttpResponseRedirect("/")


@csrf_exempt
def new_newsletter(request):
    '''assync method - add email to newsletter'''
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

class newsletterView(TemplateView):
    '''return newsletter list to admin page'''

    template_name = "admin/newsletter/list_newsletter.html"

    def get_context_data(self, **kwargs):
        return {'newsletter':Newsletter.objects.filter()}

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(newsletterView, self).dispatch(*args, **kwargs)

def handler404(request):
    ''' intercept not found page '''
    response = render(request, '404.html', {})
    response.status_code = 404
    return response
