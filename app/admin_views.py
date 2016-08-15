# -*- coding: utf-8 -*-
from app.models import Configuracao
from app.forms import ConfiguracoesForm, RedesSociaisForm
from django.template import loader, Context, RequestContext
from django.shortcuts import render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.contrib.admin.views.decorators import staff_member_required

def configuracoes_gerais(request):
    response = {'title': 'Modificando Configurações Gerais'}
    if request.method == "POST":
        configuracoesForm = ConfiguracoesForm(request.POST, request.FILES)
        
        if not configuracoesForm.is_valid():
            response.update({'form': configuracoesForm, 'errors': configuracoesForm.errors})
        else:
            configuracoesForm.save()
            
            # Configurações salvas, mostra mensagem de sucesso
            configuracoes = Configuracao.recupera_dicionario()
            configuracoesForm = ConfiguracoesForm(configuracoes)
            response.update({'form': configuracoesForm, 
                             'logomarca': configuracoes["logomarca"], 
                             'messages': ["As configurações gerais foram modificadas com sucesso!"] })
                             
            return render_to_response('admin/configuracoes/configuracoes_gerais.html', response, RequestContext(request, {}))
    else:
        # Recuperando as configurações atuais
        configuracoes = Configuracao.recupera_dicionario()
        configuracoesForm = ConfiguracoesForm(configuracoes)
        response.update({'form': configuracoesForm, 'logomarca': configuracoes["logomarca"] })
    
    return render_to_response('admin/configuracoes/configuracoes_gerais.html', response, RequestContext(request, {}))
    
    
def redes_sociais(request):
    response = {'title': 'Modificando Redes Sociais'}
    if request.method == "POST":
        redesSociaisForm = RedesSociaisForm(request.POST)
        
        if not redesSociaisForm.is_valid():
            response.update({'form': redesSociaisForm, 'errors': redesSociaisForm.errors})
        else:
            redesSociaisForm.save()
            
            # Redes sociais, mostra mensagem de sucesso
            redesSociaisForm = RedesSociaisForm(Configuracao.recupera_dicionario())
            response.update({'form': redesSociaisForm,
                             'messages': ["As Redes Sociais foram modificadas com sucesso!"] })
                             
            return render_to_response('admin/configuracoes/redes_sociais.html', response, RequestContext(request, {}))
    else:
        # Recuperando as redes sociais
        redesSociaisForm = RedesSociaisForm(Configuracao.recupera_dicionario())
        response.update({'form': redesSociaisForm})
    
    return render_to_response('admin/configuracoes/redes_sociais.html', response, RequestContext(request, {}))
    
    
def export_newsletter(request):
    response = {'title': 'Lista de pessoas cadastradas na Newsletter'}
    
    # Recuperando as pessoas da newsletter
    newsletter = Newsletter.objects.all()
    response.update({'newsletter': newsletter})

    return render_to_response('admin/app/newsletter/newsletter_export.html', response, RequestContext(request, {}))
