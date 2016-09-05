# -*- coding: utf-8 -*-
"""
    AH Website - LFMarques - 2016
    luizfelipe.unesp@gmail.com
"""
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from app.forms import ContactForm
from django.http import HttpResponse,HttpResponseRedirect
import json

def home(request):
	return render(request, 'index.html', {'is_index':True})

def about_company(request):
	return render(request, 'about_company.html', {})

def talk_with_us(request):
	return render(request, 'talk-with-us.html', {})

@csrf_exempt
def new_contact(request,contact_type):
    '''
    	send contact email
    	:params:
    		contact_type: str - contact (to user email contact) or apply_job (user sending CV)
    '''
    import ipdb; ipdb.set_trace()
    if request.method == "POST":
        
        if contact_type == 'contact':
        	contactForm = ContactForm(request.POST)
        # elif contact_type == 'apply_job':
        # 	contactForm = ContactForm(request.POST)
        # else:
        # 	contactForm = ContactForm(request.POST)
        
        return_data = {'success': True}
        if not contactForm.is_valid():
            return_data = {'success': False, 'errors' : [(k, v[0]) for k, v in contactForm.errors.items()] }
        else:
            contactForm.send(request)
        return HttpResponse(json.dumps(return_data, ensure_ascii=False)) #, content_type='application/json; charset=UTF-8'
    else:
        return HttpResponseRedirect("/")
