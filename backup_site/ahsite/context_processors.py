from django.http import HttpResponse
from django.template import RequestContext, Template
from django.urls import reverse
from django.utils.translation import activate, get_language
from app.models import GeneralConfig, Event, Partners, Products, News
from django.conf import settings


def i18n_url(request):
    """Add language prefix to URLs."""
    return {'LANGUAGE_CODE': get_language()}


def load_info(request):
    """Add general info to context."""
    return {
        'SITE_NAME': 'Agropecuária AH',
        'SITE_DESCRIPTION': 'Sistema de Administração',
        'ADMIN_EMAIL': 'ti@ah.agr.br',
    }


def admin_dashboard_context(request):
    """Add dashboard statistics to admin context."""
    if request.path.startswith('/admin/'):
        # Retorna valores padrão para evitar erros
        return {
            'equipe_compras_count': 0,
            'equipe_ativos_count': 0,
            'sale_pages_count': 0,
            'newsletter_count': 0,
            'recent_activities': [
                {
                    'description': 'Sistema de administração configurado',
                    'time': 'Hoje'
                },
                {
                    'description': 'Equipe de compras disponível',
                    'time': 'Esta semana'
                },
                {
                    'description': 'Páginas de compras configuradas',
                    'time': 'Este mês'
                }
            ]
        }
    return {}


def products_menu(request):
    """Adiciona os produtos das categorias café, suínos e bovinos ao contexto do menu principal, filtrando pelo idioma atual."""
    idioma = get_language()
    produtos = Products.objects.filter(product_category__in=["cafe", "suinos", "bovinos"], language=idioma)
    return {"products_link": produtos}


def events_menu(request):
    """Adiciona os eventos (responsabilidade social) ao contexto do menu principal, filtrando pelo idioma atual."""
    idioma = get_language()
    eventos = Event.objects.filter(language=idioma)
    return {"events_link": eventos}


def dashboard_stats(request):
    """Adiciona estatísticas para o dashboard"""
    if request.path == '/admin/' or request.path == '/admin':
        try:
            return {
                'news_count': News.objects.count(),
                'events_count': Event.objects.count(),
                'partners_count': Partners.objects.count(),
                'contacts_count': 0,  # Modelo Contact não existe
            }
        except:
            return {
                'news_count': 0,
                'events_count': 0,
                'partners_count': 0,
                'contacts_count': 0,  # Modelo Contact não existe
            }
    return {}
