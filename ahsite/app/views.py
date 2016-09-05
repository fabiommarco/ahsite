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
from app.models import Jobs

import json

def home(request):
	return render(request, 'index.html', {'is_index':True})

def about_company(request):
	return render(request, 'about_company.html', {})

def talk_with_us(request):
	context = {'url_contact':reverse('new_contact', args=['contact'])}
	print context

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

        if contact_type == 'contact':
        	contactForm = ContactForm(request.POST)
        elif contact_type == 'apply_job':
        	contactForm = ApplyJobForm(request.POST)
        else:
        	return_data = {'success': False}
        
        if not contactForm.is_valid():
            return_data = {'success': False, 'errors' : [(k, v[0]) for k, v in contactForm.errors.items()] }
        else:
            contactForm.send(request)
        return HttpResponse(json.dumps(return_data, ensure_ascii=False)) #, content_type='application/json; charset=UTF-8'
    else:
        return HttpResponseRedirect("/")
