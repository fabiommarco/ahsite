# -*- coding: utf-8 -*-
"""
    AH Website -
    Fabio Marco - 2025
      fabio.marco@ah.agr.br

"""
import functools
import json
import random
import os
import subprocess

from app.forms import ApplyJobForm, ContactForm, NewsletterForm
from app.models import *
from app.utils import reload_sys
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import get_language, gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST

colors = [
    "c8d6b9",
    "faf3dd",
    "9dbad5",
    "769ecb",
    "f6cacb",
    "d99294",
    "d4cfbd",
    "e1cec9",
    "b4bad4",
    "d2c1ce",
    "dfd8dc",
    "ebe6e5",
    "70A1D7",
    "A1DE93",
    "F7F48B",
    "F47C7C",
    "FFF9AA",
    "FFD5B8",
    "FFB9B3",
    "ACECD5",
]

# -*- coding: utf-8 -*-
"""
    AH Website -
    Fabio Marco - 2025
      fabio.marco@ah.agr.br

"""
import functools
import json
import random
import os
import subprocess

from app.forms import ApplyJobForm, ContactForm, NewsletterForm
from app.models import *
from app.utils import reload_sys
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import get_language, gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST

colors = [
    "c8d6b9",
    "faf3dd",
    "9dbad5",
    "769ecb",
    "f6cacb",
    "d99294",
    "d4cfbd",
    "e1cec9",
    "b4bad4",
    "d2c1ce",
    "dfd8dc",
    "ebe6e5",
    "70A1D7",
    "A1DE93",
    "F7F48B",
    "F47C7C",
    "FFF9AA",
    "FFD5B8",
    "FFB9B3",
    "ACECD5",
]

# -*- coding: utf-8 -*-
"""
    AH Website -
    Fabio Marco - 2025
      fabio.marco@ah.agr.br

"""
import functools
import json
import random
import os
import subprocess

from app.forms import ApplyJobForm, ContactForm, NewsletterForm
from app.models import *
from app.utils import reload_sys
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import get_language, gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST

colors = [
    "c8d6b9",
    "faf3dd",
    "9dbad5",
    "769ecb",
    "f6cacb",
    "d99294",
    "d4cfbd",
    "e1cec9",
    "b4bad4",
    "d2c1ce",
    "dfd8dc",
    "ebe6e5",
    "70A1D7",
    "A1DE93",
    "F7F48B",
    "F47C7C",
    "FFF9AA",
    "FFD5B8",
    "FFB9B3",
    "ACECD5",
]


def get_or_redirect(model, language, view_name, **kwargs):
    object = get_object_or_404(model, **kwargs)
    # Custom handling if object's language does not match current langugage.
    if object.language != language:
        # Object has a parent, therefore it is a translation.
        if object.parent:
            if object.parent.language == language:
                # Parent's object language is the current language. Simply
                # retun the parent object itself.
                translated = object.parent
            else:
                # Parent's object is not the current language. Find an object
                # whose parent is the same as its own parent.
                translated = get_object_or_404(
                    model.translated_objects, parent=object.parent
                )
        else:
            # Object does not have a parent, therefore it *is* a parent.
            # Find a translation whose parent is this object.
            translated = get_object_or_404(model.translated_objects, parent=object)
        kwargs = {k: getattr(translated, k) for k in kwargs.keys()}
        return redirect(reverse(view_name, kwargs=kwargs))
    return object


def home(request):
    """return homepage"""
    latest_feeds = News.translated_objects.order_by("-news_date")[:4]
    farms = Farm.objects.all()
    banners = []

    for farm in farms:
        farm.initials = "".join([item[0] for item in farm.farm_name.split(" ")[0:2]])
        farm.color = random.choice(colors)

    return render(
        request,
        "index.html",
        {
            "is_index": True,
            "products": Products.translated_objects.all(),
            "news": latest_feeds,
            "farms": farms,
            "banners": banners,
        },
    )


def about_company(request):
    """return about us"""
    try:
        about = AboutCompany.translated_objects.latest("id")
    except AboutCompany.DoesNotExist:
        about = None
    timeline = TimeLine.translated_objects.all().order_by("year")

    return render(request, "about_company.html", {"about": about, "timeline": timeline})


def agricutural_prices(request):
    """return agricultural prices page"""
    prices = AgriculturalFiles.objects.order_by("-ap_date")[:5]
    return render(request, "agricutural_prices.html", {"prices": prices})


def brasilandia_ms_history(request):
    """return A História e memória de Brasilândia/MS page - static html"""
    return render(
        request,
        "brasilandia_history_{language}.html".format(language=get_language())
    )


def environmental_responsability(request):
    """return environmental responsability page"""
    language = request.LANGUAGE_CODE
    context = {}
    try:
        environ = EnvironmentalResponsability.objects.get(language=language)
        context["environ"] = environ
    except EnvironmentalResponsability.DoesNotExist:
        try:
            environ = EnvironmentalResponsability.objects.get(language="pt")
            context["environ"] = environ
        except EnvironmentalResponsability.DoesNotExist:
            pass
            
    return render(request, "environmental.html", context)


def event_view(request, event_slug=None):
    """return event details page"""
    event = get_or_redirect(
        Event,
        language=request.LANGUAGE_CODE,
        view_name="event_view",
        event_slug=event_slug,
    )
    if not isinstance(event, Event):
        return event
    # Listar imagens da pasta static/img/social/
    fotos = [
        'WhatsApp Image 2025-07-02 at 08.50.23.jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.24.jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.24 (1).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.24 (2).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.24 (3).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.24 (4).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.25.jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.25 (1).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.25 (2).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.26.jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.26 (1).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.26 (2).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.26 (3).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.27.jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.27 (1).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.27 (2).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.27 (3).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.28.jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.28 (1).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.28 (2).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.29.jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.29 (1).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.29 (2).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.29 (3).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.30.jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.30 (1).jpeg',
    ]
    return render(request, "event_view.html", {"event": event, "fotos": fotos})


def partners_view(request, partner_slug=None):
    """return partners view page"""
    partner = get_or_redirect(
        Partners,
        language=request.LANGUAGE_CODE,
        view_name="partners_view",
        partner_slug=partner_slug,
    )
    if not isinstance(partner, Partners):
        return partner
    return render(request, "partners_view.html", {"partner": partner})


def news(request):
    """return lastest news"""
    # Busca todas as notícias e ordena por data
    all_news = News.objects.order_by("-news_date")
    
    # Filtra por idioma
    language = request.LANGUAGE_CODE
    filtered_news = []
    for news in all_news:
        if news.language == language:
            filtered_news.append(news)
        elif news.parent and news.parent.language == language:
            filtered_news.append(news.parent)
    
    # Configura a paginação
    paginator = Paginator(filtered_news, 6)

    try:
        page = int(request.GET.get("page", 1))
    except ValueError:
        page = 1

    try:
        news_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        news_page = paginator.page(paginator.num_pages)

    return render(request, "news.html", {
        "all_news": news_page,
        "page_obj": news_page,
        "is_paginated": paginator.num_pages > 1
    })


def news_view(request, news_slug=None):
    """return news details"""
    # Busca a notícia pelo slug
    news = get_object_or_404(News, news_slug=news_slug)
    
    # Verifica se precisa redirecionar para a versão no idioma correto
    language = request.LANGUAGE_CODE
    if news.language != language:
        if news.parent and news.parent.language == language:
            news = news.parent
        else:
            # Busca uma tradução no idioma correto
            translated = News.objects.filter(parent=news, language=language).first()
            if translated:
                news = translated
    
    return render(request, "news_view.html", {"news": news})


def sales(request):
    """return sales page"""
    equipe_compras = EquipeCompras.objects.filter(ativo=True).order_by('ordem', 'nome')
    return render(
        request,
        "sales.html",
        {
            "sale": Sale.translated_objects.latest("id"),
            "url_contact": reverse("new_contact", args=["sale"]),
            "equipe_compras": equipe_compras,
        },
    )


def magazine(request):
    """return all magazines"""
    magazines = Magazine.objects.order_by("-magazine_date")
    magazine = magazines[0] if magazines else None
    return render(
        request, "magazine.html", {
            "magazine": magazine,
            "all_magazines": magazines
        }
    )


def product_view(request, product_slug=None):
    """return products details page"""
    product = get_or_redirect(
        Products,
        language=request.LANGUAGE_CODE,
        view_name="product_view",
        product_slug=product_slug,
    )
    if not isinstance(product, Products):
        return product
    choices = settings.BANNER_IMG.get(product.product_category)
    rand_img = random.choice(choices or random.randrange(1, 11))
    return render(
        request, "product_view.html", {"product": product, "random_img": rand_img}
    )


def talk_with_us(request):
    """return contact page"""
    return render(
        request,
        "talk-with-us.html",
        {"url_contact": reverse("new_contact", args=["contact"])},
    )


def work_with_us(request):
    """return careers page"""
    return render(
        request,
        "work-with-us.html",
        {
            "jobs": Jobs.objects.filter(),
            "is_apply_job": True,
            "url_contact": reverse("new_contact", args=["apply_job"]),
        },
    )


@csrf_exempt
def new_contact(request, contact_type):
    """
        send contact email
        :params:
            contact_type: str - contact (to user email contact) or apply_job (user sending CV)
    """
    if request.method == "POST":
        return_data = {"success": True}
        apply_job_context = False
        if contact_type == "contact" or contact_type == "sale":
            contact_form = ContactForm(request.POST)
        elif contact_type == "apply_job":
            contact_form = ApplyJobForm(request.POST, request.FILES)
            apply_job_context = True
        else:
            return_data = {"success": False}

        if not contact_form.is_valid():
            return_data = {
                "success": False,
                "errors": [(k, v[0]) for k, v in contact_form.errors.items()],
            }
            messages.add_message(
                request,
                messages.ERROR,
                _(
                    "Parece que algo de errado aconteceu. Por favor, tente novamente mais tarde!"
                ),
            )
        else:
            if contact_type == "sale":
                extra_recipient = Sale.translated_objects.latest("id")
                success, error_msg = contact_form.send(request, extra_recipient.sale_email)
            else:
                success, error_msg = contact_form.send(request)
            if success:
                messages.add_message(
                    request, messages.SUCCESS, _( "Obrigado! Sua mensagem foi enviada.")
                )
            else:
                messages.add_message(
                    request, messages.ERROR, _("Erro ao enviar e-mail: ") + error_msg
                )
                return_data = {"success": False, "error": error_msg}
        if apply_job_context:
            return HttpResponseRedirect(reverse("work_with_us", args=()))
        return HttpResponse(json.dumps(return_data, ensure_ascii=False))

    return HttpResponseRedirect("/")


@csrf_exempt
def new_newsletter(request):
    """assync method - add email to newsletter"""
    if request.method == "POST":
        newsletter_form = NewsletterForm(request.POST)
        data = {"success": True}
        if not newsletter_form.is_valid():
            data = {
                "success": False,
                "errors": [(k, v[0]) for k, v in newsletter_form.errors.items()],
            }
        else:
            newsletter_form.save()
        return HttpResponse(json.dumps(data, ensure_ascii=False))
    return HttpResponseRedirect("/")


class newsletterView(TemplateView):
    """return newsletter list to admin page"""

    template_name = "admin/newsletter/list_newsletter.html"

    def get_context_data(self, **kwargs):
        return {"newsletter": Newsletter.objects.filter()}

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(newsletterView, self).dispatch(*args, **kwargs)


def handler404(request):
    """ intercept not found page """
    response = render(request, "404.html", {})
    response.status_code = 404
    return response


def denuncia_view(request):
    return render(request, 'denuncia.html')


def convert_year_to_integer(apps, schema_editor):
    Timeline = apps.get_model('app', 'Timeline')
    for timeline in Timeline.objects.all():
        try:
            # Se for objeto de data
            if hasattr(timeline.year, 'year'):
                year = timeline.year.year
            # Se for string numérica
            elif isinstance(timeline.year, str) and timeline.year.isdigit():
                year = int(timeline.year)
            # Se for string tipo '2020-01-01'
            elif isinstance(timeline.year, str):
                year = int(timeline.year[:4])
            # Se for inteiro
            elif isinstance(timeline.year, int):
                year = timeline.year
            else:
                year = 2020  # valor padrão
            # Atualiza diretamente no banco, sem chamar save()
            Timeline.objects.filter(pk=timeline.pk).update(year_temp=year)
        except Exception as e:
            Timeline.objects.filter(pk=timeline.pk).update(year_temp=2020)


@csrf_exempt
@require_POST
def deploy_webhook(request):
    """
    Webhook para deploy automático via GitHub
    """
    try:
        # Verificar se é um push para a branch main
        payload = request.body.decode('utf-8')
        
        # Executar o deploy
        try:
            output = subprocess.check_output([
                'bash', '/var/www/ahsite_news/ahsite/backup_site/deploy.sh'
            ], cwd='/var/www/ahsite_news/ahsite/ahsite', stderr=subprocess.STDOUT)
            
            # Converter bytes para string
            output_str = output.decode('utf-8') if isinstance(output, bytes) else str(output)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Deploy realizado com sucesso!',
                'output': output_str
            })
        except subprocess.CalledProcessError as e:
            # Converter bytes para string
            error_output = e.output.decode('utf-8') if isinstance(e.output, bytes) else str(e.output)
            
            return JsonResponse({
                'status': 'error',
                'message': 'Erro no deploy',
                'output': error_output
            }, status=500)
            
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


def deploy_page(request):
    """
    Página com botão de deploy
    """
    return render(request, 'deploy.html')


def robots_txt(request):
    """Serve robots.txt dinamicamente"""
    content = """User-agent: *
Allow: /
Sitemap: https://www.agropecuariaah.agr.br/sitemap.xml"""
    return HttpResponse(content, content_type='text/plain')


@csrf_exempt
@require_POST
def deploy_webhook(request):
    """Webhook para deploy automático via GitHub"""
    try:
        # Verificar se é um push para a branch main
        payload = request.body.decode('utf-8')
        
        # Executar o deploy
        result = subprocess.check_output([
            'bash', '/var/www/ahsite_news/ahsite/backup_site/deploy.sh'
        ], stderr=subprocess.STDOUT, cwd='/var/www/ahsite_news/ahsite/ahsite')
        
        # Decodificar o resultado para string
        result_str = result.decode('utf-8')
        
        return JsonResponse({
            'status': 'success',
            'message': 'Deploy realizado com sucesso!',
            'output': result_str
        })
            
    except subprocess.CalledProcessError as e:
        return JsonResponse({
            'status': 'error',
            'message': 'Erro no deploy',
            'output': e.output.decode('utf-8') if e.output else str(e)
        }, status=500)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@staff_member_required
def admin_deploy_view(request):
    """View para deploy via painel admin"""
    if request.method == 'POST':
        try:
            # Executar o deploy
            result = subprocess.check_output([
                'bash', '/var/www/ahsite_news/ahsite/backup_site/deploy.sh'
            ], stderr=subprocess.STDOUT, cwd='/var/www/ahsite_news/ahsite/ahsite')
            
            result_str = result.decode('utf-8')
            messages.success(request, f'Deploy realizado com sucesso! {result_str}')
            
        except subprocess.CalledProcessError as e:
            error_msg = e.output.decode('utf-8') if e.output else str(e)
            messages.error(request, f'Erro no deploy: {error_msg}')
        except Exception as e:
            messages.error(request, f'Erro inesperado: {str(e)}')
    
    return render(request, 'admin_deploy.html')


def deploy_page(request):
    """Página com botão de deploy"""
    return render(request, 'deploy.html')


def robots_txt(request):
    """Serve robots.txt dinamicamente"""
    content = """User-agent: *
Allow: /
Sitemap: https://www.agropecuariaah.agr.br/sitemap.xml"""
    return HttpResponse(content, content_type='text/plain')


@csrf_exempt
@require_POST
def deploy_webhook(request):
    """Webhook para deploy automático via GitHub"""
    try:
        # Verificar se é um push para a branch main
        payload = request.body.decode('utf-8')
        
        # Executar o deploy
        result = subprocess.check_output([
            'bash', '/var/www/ahsite_news/ahsite/backup_site/deploy.sh'
        ], stderr=subprocess.STDOUT, cwd='/var/www/ahsite_news/ahsite/ahsite')
        
        # Decodificar o resultado para string
        result_str = result.decode('utf-8')
        
        return JsonResponse({
            'status': 'success',
            'message': 'Deploy realizado com sucesso!',
            'output': result_str
        })
            
    except subprocess.CalledProcessError as e:
        return JsonResponse({
            'status': 'error',
            'message': 'Erro no deploy',
            'output': e.output.decode('utf-8') if e.output else str(e)
        }, status=500)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@staff_member_required
def admin_deploy_view(request):
    """View para deploy via painel admin"""
    if request.method == 'POST':
        try:
            # Executar o deploy
            result = subprocess.check_output([
                'bash', '/var/www/ahsite_news/ahsite/backup_site/deploy.sh'
            ], stderr=subprocess.STDOUT, cwd='/var/www/ahsite_news/ahsite/ahsite')
            
            result_str = result.decode('utf-8')
            messages.success(request, f'Deploy realizado com sucesso! {result_str}')
            
        except subprocess.CalledProcessError as e:
            error_msg = e.output.decode('utf-8') if e.output else str(e)
            messages.error(request, f'Erro no deploy: {error_msg}')
        except Exception as e:
            messages.error(request, f'Erro inesperado: {str(e)}')
    
    return render(request, 'admin_deploy.html')


def deploy_page(request):
    """Página com botão de deploy"""
    return render(request, 'deploy.html')


@staff_member_required
def commit_automatico_view(request):
    """View para commit automático via painel admin"""
    if request.method == 'POST':
        try:
            # Executar o script de commit automático
            resultado = subprocess.check_output([
                'python', 'commit_automatico.py'
            ], stderr=subprocess.STDOUT, cwd='/var/www/ahsite_news/ahsite/backup_site')
            
            resultado_str = resultado.decode('utf-8')
            messages.success(request, f'Commit automático realizado com sucesso! {resultado_str}')
            
        except subprocess.CalledProcessError as e:
            error_msg = e.output.decode('utf-8') if e.output else str(e)
            messages.error(request, f'Erro no commit automático: {error_msg}')
        except Exception as e:
            messages.error(request, f'Erro inesperado: {str(e)}')
    
    return render(request, 'commit_automatico.html')
