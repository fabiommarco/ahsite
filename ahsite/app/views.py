# -*- coding: utf-8 -*-
"""
    AH Website - LFMarques - 2016
    luizfelipe.unesp@gmail.com
"""
from django.shortcuts import render

def home(request):
	return render(request, 'index.html', {'is_index':True})

def about_company(request):
	return render(request, 'about_company.html', {})