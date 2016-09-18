"""

"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url, include
from app import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    url(r'^$', views.home, name='home'),
    url(r'^quem-somos/$', views.about_company, name='about_company'),
    url(r'^cotacoes-agricolas/$', views.agricutural_prices, name='agricutural_prices'),

    # url(r'^responsabilidade-social/$', views.events, name='events'),
    url(r'^responsabilidade-social/(?P<event_slug>.*)$', views.event_view, name='event_view'),

    url(r'^compras/$', views.sales, name='sales'),
    url(r'^vendas/$', views.products_list, name='products_list'),
    url(r'^vendas/(?P<product_slug>.*)$', views.product_view, name='product_view'),

    url(r'^noticias/$', views.news, name='news'),
    url(r'^noticias/(?P<news_slug>.*)$', views.news_view, name='news_view'),

    url(r'^parcerias/(?P<partner_slug>.*)$', views.partners_view, name='partners_view'),

    url(r'^revista-pagina-um/$', views.magazine, name='magazine'),

    url(r'^fale-conosco/$', views.talk_with_us, name='talk_with_us'),
    url(r'^trabalhe-conosco/$', views.work_with_us, name='work_with_us'),

    url(r'^new_contact/(?P<contact_type>.*)$', views.new_contact, name='new_contact'),
    url(r'^newsletter/$', views.new_newsletter, name='new_newsletter'),

    #includes
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/list_newsletter$', views.list_newsletter, name='list_newsletter'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)