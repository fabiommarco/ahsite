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
    
    url(r'^responsabilidade-social/$', views.events, name='events'),
    url(r'^responsabilidade-social/(?P<event_slug>.*)$', views.event_view, name='event_view'),
    
    url(r'^vendas/$', views.sales, name='sales'),

    url(r'^noticias/$', views.news, name='news'),
    url(r'^noticias/(?P<news_slug>.*)$', views.news_view, name='news_view'),
    

    url(r'^fale-conosco/$', views.talk_with_us, name='talk_with_us'),
    url(r'^trabalhe-conosco/$', views.work_with_us, name='work_with_us'),
    
    url(r'^new_contact/(?P<contact_type>.*)$', views.new_contact, name='new_contact'),
    
	#includes
	url(r'^grappelli/', include('grappelli.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    #admin
    url(r'^admin/', admin.site.urls),

    # Media
    # url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # url(r'^media/admin/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT + 'admin/'}),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)