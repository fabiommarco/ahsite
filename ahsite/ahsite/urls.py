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
    url(r'^fale-conosco/$', views.talk_with_us, name='talk_with_us'),
    url(r'^trabalhe-conosco/$', views.work_with_us, name='work_with_us'),
    
    url(r'^new_contact/(?P<contact_type>.*)$', views.new_contact, name='new_contact'),
    
	#includes
	url(r'^grappelli/', include('grappelli.urls')),
    #admin
    url(r'^admin/', admin.site.urls),

]