"""

"""
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.conf.urls import url, include
from app import views

from django.conf import settings
from django.conf.urls.static import static
from app.views import newsletterView

urlpatterns = (
    [url(r"^i18n/", include("django.conf.urls.i18n"))]
    + i18n_patterns(
        url(r"^$", views.home, name="home"),
        url(_(r"^quem-somos/$"), views.about_company, name="about_company"),
        url(
            _(r"^brasilandia-ms-history/$"),
            views.brasilandia_ms_history,
             name="brasilandia_ms_history"
        ),
        url(
            _(r"^cotacoes-agricolas/$"),
            views.agricutural_prices,
            name="agricutural_prices",
        ),
        url(
            _(r"^responsabilidade-ambiental/$"),
            views.environmental_responsability,
            name="environmental_responsability",
        ),
        url(
            _(r"^responsabilidade-social/(?P<event_slug>.*)$"),
            views.event_view,
            name="event_view",
        ),
        url(_(r"^compras/$"), views.sales, name="sales"),
        url(
            _(r"^vendas/(?P<product_slug>.*)$"), views.product_view, name="product_view"
        ),
        url(_(r"^noticias/$"), views.news, name="news"),
        url(_(r"^noticias/(?P<news_slug>.*)$"), views.news_view, name="news_view"),
        url(
            _(r"^parcerias/(?P<partner_slug>.*)$"),
            views.partners_view,
            name="partners_view",
        ),
        url(_(r"^revista-pagina-um/$"), views.magazine, name="magazine"),
        url(_(r"^fale-conosco/$"), views.talk_with_us, name="talk_with_us"),
        url(_(r"^trabalhe-conosco/$"), views.work_with_us, name="work_with_us"),
        url(r"^newsletter/$", views.new_newsletter, name="new_newsletter"),
        url(
            r"^new_contact/(?P<contact_type>.*)$", views.new_contact, name="new_contact"
        ),
        # admin
        url(r"^grappelli/", include("grappelli.urls")),
        url(r"^ckeditor/", include("ckeditor_uploader.urls")),
        url(r"^admin/", admin.site.urls),
        url(r"^admin/list_newsletter/$", newsletterView.as_view()),
        prefix_default_language=False,
    )
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
