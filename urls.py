# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',

    
    # Paginas
    (r'^$', 'app.views.home'),    
# Página Inicial
    (r'^quem-somos/$','app.views.quem_somos'),                                                           # Quem-Somos
    (r'^noticias/$','app.views.noticias'),                                                               # Notícias
    (r'^noticias/todas/$','app.views.list_noticias'),                                                    # Notícias Todas
    (r'^noticias/(?P<id>.*)/(?P<slug>.*)/$','app.views.view_noticia'),                                   # Notícias Particular
    (r'^produtos/$','app.views.produtos'),                                                               # Produtos
    (r'^produtos/categorias/(?P<categoria_id>.*)/(?P<categoria_slug>.*)$','app.views.produtos'),         # Produtos por Categoria    
    (r'^produtos/(?P<produto_id>.*)/(?P<slug>.*)/$','app.views.view_produto'),                           # Produtos Detalhes
    (r'^servicos/$','app.views.servicos'),                                                               # Servicos
    (r'^servicos/(?P<servico_id>.*)/(?P<slug>.*)/$','app.views.view_servico'),                           # Serviços Detalhes
    (r'^clientes/$','app.views.clientes'),                                                               # Clientes
    (r'^clientes/(?P<cliente_id>.*)/(?P<slug>.*)$','app.views.view_cliente'),                           # Clientes Detalhes
    (r'^contato/$','app.views.contato'),                                                                 # Contato









	# Css
    (r'^css/main.css$', 'app.views.css'),
    
    # Media
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
    
    # Grappelli
    (r'^grappelli/', include('grappelli.urls')),
    
    # Configurações Gerais
    (r'^admin/configuracoes-gerais/$', 'app.admin_views.configuracoes_gerais'),
    (r'^admin/redes-sociais/$', 'app.admin_views.redes_sociais'),
    (r'^admin/export/newsletter/$', 'app.admin_views.export_newsletter'),

	 # Busca
    (r'^search/$', 'app.views.search'),                                            # Search
    
    # Retorno AJAX
    (r'^contato/new/$', 'app.views.new_contato'),
    (r'^newsletter/new/$', 'app.views.new_newsletter'),
    
    # Css
    (r'^css/main.css$', 'app.views.css'),
    
    # Media
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^media/admin/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT + 'admin/'}),
    
    # Grappelli
    (r'^grappelli/', include('grappelli.urls')),
    
    
    # Admin
    (r'^admin/', include(admin.site.urls)),              

                                                          
 
)
