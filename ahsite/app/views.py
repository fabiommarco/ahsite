# -*- coding: utf-8 -*-
"""
    AH Website - LFMarques - 2016
    luizfelipe.unesp@gmail.com
"""
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from app.forms import ContactForm,ApplyJobForm
from app.models import Jobs, AboutCompany, GeneralConfig
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

def home(request):
    return render(request, 'index.html', {'is_index':True})

@load_basic_info
def about_company(request,r=None):
    about = AboutCompany.objects.latest('id')
    return render(request, 'about_company.html', {'about':about,'general_info':general_info})

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
    # from django.contrib.messages import constants as messages
    from django.contrib import messages
    if request.method == "POST":
        return_data = {'success': True}
        apply_job_context = False
    
        if contact_type == 'contact':
            contactForm = ContactForm(request.POST)
        elif contact_type == 'apply_job':
            contactForm = ApplyJobForm(request.POST, request.FILES)
            apply_job_context = True
        else:
            return_data = {'success': False}
        
        if not contactForm.is_valid():
            return_data = {'success': False, 'errors' : [(k, v[0]) for k, v in contactForm.errors.items()] }
            messages.add_message(request, messages.ERROR, 'Parece que algo de errado aconteceu . Por favor, tente novamente mais tarde!')
        else:
            contactForm.send(request)
            messages.add_message(request, messages.SUCCESS, 'Obrigado! Sua mensagem foi enviada.')
        if apply_job_context:
            # return render(request, 'work-with-us.html', {})
            return HttpResponseRedirect(reverse('work_with_us', args=()))
        return HttpResponse(json.dumps(return_data, ensure_ascii=False)) #, content_type='application/json; charset=UTF-8'
    
    return HttpResponseRedirect("/")