"""
AH Website URLs Configuration
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from app import views
from app.views import newsletterView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('grappelli/', include('grappelli.urls')),
]

urlpatterns += i18n_patterns(
    # Admin URLs - IMPORTANTE: Colocar ANTES do admin.site.urls
    path('admin/deploy/', views.admin_deploy_view, name='admin_deploy'),
    path('admin/commit/', views.commit_automatico_view, name='commit_automatico'),
    path('admin/list_newsletter/', newsletterView.as_view()),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # Site URLs
    path('', views.home, name="home"),
    path(_('quem-somos/'), views.about_company, name="about_company"),
    path(_('agropecuaria-ah/'), views.about_company, name="agropecuaria_ah"),  # URL alternativa
    path(_('brasilandia-ms-history/'), views.brasilandia_ms_history, name="brasilandia_ms_history"),
    path(_('cotacoes-agricolas/'), views.agricutural_prices, name="agricutural_prices"),
    path(_('responsabilidade-ambiental/'), views.environmental_responsability, name="environmental_responsability"),
    re_path(_(r'responsabilidade-social/(?P<event_slug>.*)$'), views.event_view, name="event_view"),
    path(_('compras/'), views.sales, name="sales"),
    re_path(_(r'vendas/(?P<product_slug>.*)$'), views.product_view, name="product_view"),
    path(_('noticias/'), views.news, name="news"),
    re_path(_(r'noticias/(?P<news_slug>.*)$'), views.news_view, name="news_view"),
    re_path(_(r'parcerias/(?P<partner_slug>.*)$'), views.partners_view, name="partners_view"),
    path(_('revista-pagina-um/'), views.magazine, name="magazine"),
    path(_('fale-conosco/'), views.talk_with_us, name="talk_with_us"),
    path(_('trabalhe-conosco/'), views.work_with_us, name="work_with_us"),
    path('newsletter/', views.new_newsletter, name="new_newsletter"),
    re_path(r'new_contact/(?P<contact_type>.*)$', views.new_contact, name="new_contact"),
    path('denuncia/', views.denuncia_view, name='denuncia'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    
    prefix_default_language=False
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('gestao/', include('gestao.urls')),
    path('deploy/', views.deploy_webhook, name='deploy_webhook'),
    path('deploy-page/', views.deploy_page, name='deploy_page'),
]
