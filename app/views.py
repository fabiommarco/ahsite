# -*- coding: utf-8 -*-
from django.template import loader, Context, RequestContext
from django.shortcuts import render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt


from app.models import Configuracao, Noticia, Pagina,Cliente
from app.utils import getTwitts, getBanner, remove_accents
from django.utils import simplejson
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def configuracoes():
    # Configuracoes
    configuracoes = {'configuracoes': Configuracao.recupera_dicionario() }
    
    return configuracoes

def my_first_view(request):
	return HttpResponse('Hello world!')


def home(request):
    retorno = configuracoes()
   
 
    # Recuperando as notícias
    retorno.update({'noticias': Noticia.objects.order_by('-data')[:3]})
    
    
     #Recuperando os twits do usuário
    # tweets = getTwitts(retorno["configuracoes"]["twitter_username"], 6)
    # if tweets: retorno.update({'tweets': tweets })
    
    #Descobrindo o banner atual
    retorno.update({'banner': getBanner("pagina_inicial")})
    
    return render_to_response('home.html', retorno, context_instance=RequestContext(request))

def quem_somos(request):
    retorno = configuracoes()

    # Recuperando a Página de Quem Somos
    retorno.update({'quem_somos': Pagina.objects.get(id=1)})
    
    # Descobrindo o banner atual
    retorno.update({'banner': getBanner("quem_somos")})

    return render_to_response('quem-somos.html', retorno, context_instance=RequestContext(request))
    
def noticias(request):
    retorno = configuracoes()

    # Recuperando a Página de Quem Somos
    noticias = Noticia.objects.order_by('-data')[:4]
    
    if len(noticias) > 0:
        total_imagens = noticias[0].imagens.count()
        exibe_imagens = False
        if (total_imagens > 0 and not noticias[0].mostra_principal) or (total_imagens > 1 and noticias[0].mostra_principal):
            exibe_imagens = True
            
        retorno.update({'ultima_noticia': noticias[0], 'exibe_imagens': exibe_imagens, 'noticias': noticias[1:]})

    # Descobrindo o banner atual
    retorno.update({'banner': getBanner("noticias")})

    return render_to_response('noticias.html', retorno, context_instance=RequestContext(request))

def view_noticia(request, id, slug):
    retorno = configuracoes()

    # Recuperando a Página de Quem Somos
    noticia = Noticia.objects.filter(id=id).filter(slug=slug)
    if len(noticia) == 1:
        total_imagens = noticia[0].imagens.count()
        exibe_imagens = False
        if (total_imagens > 0 and not noticia[0].mostra_principal) or (total_imagens > 1 and noticia[0].mostra_principal):
            exibe_imagens = True
        
        retorno.update({'noticia': noticia[0], 'exibe_imagens': exibe_imagens})

    # Descobrindo o banner atual
    retorno.update({'banner': getBanner("noticias")})

    return render_to_response('view_noticia.html', retorno, context_instance=RequestContext(request))

def list_noticias(request):
    retorno = configuracoes()

    # Recuperando a Página de Quem Somos
    noticias = Noticia.objects.order_by('-data')
    retorno.update({'noticias': noticias})

    # Descobrindo o banner atual
    retorno.update({'banner': getBanner("noticias")})

    return render_to_response('list_noticias.html', retorno, context_instance=RequestContext(request))


def servicos(request):
    retorno = configuracoes()

    # Se a pagina de servicos não puder ser exibida, jogue um erro 404
    if retorno["configuracoes"]["exibe_servicos"] == "False": raise Http404

    # Recuperando as Categorias e suas respectivas Subcategorias
    categorias = CategoriaProduto.retorna_categorias()

    servicos = Servico.objects.order_by('nome')

    paginator = Paginator(servicos, 6)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        servicos = paginator.page(page)
    except (EmptyPage, InvalidPage):
        servicos = paginator.page(paginator.num_pages)

    # Adicionando os serviços ao dicionario que será entregue à view
    retorno.update({'servicos': servicos})

    # Descobrindo o banner atual
    retorno.update({'banner': getBanner("servicos")})

    return render_to_response('servicos.html', retorno, context_instance=RequestContext(request))

def view_servico(request, servico_id, slug):
    retorno = configuracoes()

    # Se a pagina de serviços não puder ser exibida, jogue um erro 404
    if retorno["configuracoes"]["exibe_servicos"] == "False": raise Http404

    # Recuperando o produto
    servico = Servico.objects.filter(id=servico_id).filter(slug=slug)

    # Se o serviço não for encontrado, redirecione para a home
    if len(servico) <> 1:
        return HttpResponseRedirect("/servicos/")
    else:
        servico = servico[0]

    # Adicionando as categorias e os produtos ao dicionario que será entregue à view
    retorno.update({'servico': servico})

    # Descobrindo o banner atual
    retorno.update({'banner': getBanner("servicos")})

    return render_to_response('view_servico.html', retorno, context_instance=RequestContext(request))

def clientes(request):
    retorno = configuracoes()
    
    # Recuperando a lista de Clientes
    clientes = Cliente.objects.all()
    
    # Adicionando os clientes ao dicionario que será entregue à view
    retorno.update({'clientes': clientes})
    
    # Descobrindo o banner atual
    retorno.update({'banner': getBanner("clientes")})

    return render_to_response('clientes.html', retorno, context_instance=RequestContext(request))
    
def view_cliente(request, cliente_id, slug):
    retorno = configuracoes()

    # Se a pagina de clientes não puder ser exibida, jogue um erro 404
    if retorno["configuracoes"]["exibe_clientes"] == "False": raise Http404

    # Recuperando o produto
    cliente = Cliente.objects.filter(id=cliente_id).filter(slug=slug)

    # Se o cliente não for encontrado, redirecione para a home
    if len(cliente) <> 1:
        return HttpResponseRedirect("/clientes/")
    else:
        cliente = cliente[0]

    # Adicionando os clientes ao dicionario que será entregue à view
    retorno.update({'cliente': cliente})

    # Descobrindo o banner atual
    retorno.update({'banner': getBanner("clientes")})

    return render_to_response('view_cliente.html', retorno, context_instance=RequestContext(request))

def contato(request):
    retorno = configuracoes()
    
    # Descobrindo o banner atual
    retorno.update({'banner': getBanner("contato")})
    
    return render_to_response('contato.html', retorno, context_instance=RequestContext(request))

def search(request):
    from haystack.query import SearchQuerySet
    
    retorno = configuracoes()
    
    try: 
        # Keyword
        retorno.update({'keyword': request.GET.get("q")})
        
        # sterm
        sTerm = remove_accents(request.GET.get('q'))
    except: 
        return HttpResponseRedirect('/')
        
    results = SearchQuerySet().auto_query(remove_accents(sTerm))
    retorno.update({'results': results})
    print results
    
    # print dir(results[0])

    # Descobrindo o banner atual
    retorno.update({'banner': getBanner("pagina_inicial")})
    
    return render_to_response('search.html', retorno, context_instance=RequestContext(request))

def css(request):
    configuracoes_dict = configuracoes()
    
    th = loader.get_template('main.css')
    c = Context({
         'cor_layout': configuracoes_dict["configuracoes"]["cor_layout"]
    })
    css = th.render(c)
    
    return HttpResponse(css, content_type="text/css")

@csrf_exempt    
def new_newsletter(request):
    if request.method == "POST":
        newsletterForm = NewsletterForm(request.POST)
        json = {'success': True}
        if not newsletterForm.is_valid():
            json = {'success': False, 'errors' : [(k, v[0]) for k, v in newsletterForm.errors.items()] }
        else:
            newsletterForm.save()
        return HttpResponse(simplejson.dumps(json, ensure_ascii=False)) #, content_type='application/json; charset=UTF-8'
    else:
        return HttpResponseRedirect("/")
        
def new_contato(request):
    if request.method == "POST":
        contatoForm = ContatoForm(request.POST)
        json = {'success': True}
        if not contatoForm.is_valid():
            json = {'success': False, 'errors' : [(k, v[0]) for k, v in contatoForm.errors.items()] }
        else:
            contatoForm.send(configuracoes=configuracoes())
        return HttpResponse(simplejson.dumps(json, ensure_ascii=False)) #, content_type='application/json; charset=UTF-8'
    else:
        return HttpResponseRedirect("/")
