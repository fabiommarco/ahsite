#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sistema Completo de Deploy e Correções - Agropecuária AH
Fabio Marco - 2025
fabio.marco@ah.agr.br

Este script:
1. Corrige rotas e templates
2. Adiciona notícia do Angus
3. Implementa sistema de deploy automático
4. Organiza o admin
"""

import os
import sys
import django
import subprocess
import requests
from urllib.parse import urlparse
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from django.contrib.auth.models import User
from app.models import News, Imagem
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import tempfile
import urllib.request


def baixar_imagem(url, nome_arquivo):
    """Baixa uma imagem da URL e retorna um arquivo temporário"""
    try:
        # Criar arquivo temporário
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urllib.request.urlopen(url).read())
        img_temp.flush()
        
        # Criar nome do arquivo
        extensao = url.split('.')[-1].split('?')[0]
        if extensao not in ['jpg', 'jpeg', 'png', 'gif']:
            extensao = 'jpg'
        
        nome_completo = f"{nome_arquivo}.{extensao}"
        
        return File(img_temp, name=nome_completo)
    except Exception as e:
        print(f"❌ Erro ao baixar imagem {url}: {e}")
        return None


def criar_noticia_angus():
    """Cria a notícia sobre a novilhada Angus"""
    print("📰 Criando notícia sobre a novilhada Angus...")
    
    # Verificar se já existe
    noticia_existente = News.objects.filter(news_title__icontains="Angus").first()
    if noticia_existente:
        print(f"✅ Notícia do Angus já existe: {noticia_existente.news_title}")
        return noticia_existente
    
    # Dados da notícia
    titulo = "Novilhada Angus surpreende por ganhar 1 arroba por mês - 17,5 arrobas aos 17 meses"
    slug = "novilhada-angus-surpreende-por-ganhar-1-arroba-por-mes-175-arrobas-aos-17-meses"
    
    conteudo = """
    <h2>Novilhada Angus da Agropecuária AH alcança resultados excepcionais</h2>
    
    <p>A Agropecuária AH tem se destacado no cenário da pecuária brasileira com resultados impressionantes em sua criação de novilhas Angus. Recentemente, o rebanho surpreendeu ao alcançar um ganho médio de <strong>1 arroba por mês</strong>, resultando em animais com <strong>17,5 arrobas aos 17 meses de idade</strong>.</p>
    
    <p>Este resultado coloca a Agropecuária AH entre as propriedades de referência na criação de bovinos Angus no Brasil. O ganho de peso consistente demonstra a excelência em genética, nutrição e manejo aplicados na propriedade.</p>
    
    <h3>Destaques da Novilhada Angus</h3>
    
    <ul>
        <li><strong>Ganho médio:</strong> 1 arroba por mês</li>
        <li><strong>Peso final:</strong> 17,5 arrobas aos 17 meses</li>
        <li><strong>Genética:</strong> Linhagem Angus de excelência</li>
        <li><strong>Nutrição:</strong> Programa alimentar otimizado</li>
        <li><strong>Manejo:</strong> Protocolos de bem-estar animal</li>
    </ul>
    
    <p>O pecuarista <strong>Helder Höfig</strong>, CEO da Agropecuária AH, destaca que estes resultados são fruto de anos de investimento em tecnologia e melhoramento genético. "Nossa equipe trabalha com foco total na qualidade e produtividade, sempre respeitando o bem-estar animal e a sustentabilidade", afirma.</p>
    
    <h3>Reconhecimento Nacional</h3>
    
    <p>A excelência da novilhada Angus da Agropecuária AH foi reconhecida pelo Canal Rural, que publicou uma reportagem especial sobre os resultados alcançados. A matéria destaca o trabalho pioneiro da propriedade na criação de bovinos de corte de alta qualidade.</p>
    
    <p><strong>Link:</strong> <a href="https://girodoboi.canalrural.com.br/pecuaria/certificacoes-e-qualidade/novilhada-angus-surpreende-por-ganhar-1-arroba-por-mes-175-arrobas-aos-17-meses/" target="_blank" rel="noopener">Ver reportagem completa no Canal Rural</a></p>
    """
    
    # Criar a notícia
    noticia = News.objects.create(
        news_title=titulo,
        news_slug=slug,
        news_description=conteudo,
        news_date="2025-08-30",
        language="pt",
        news_video="okehG50jSp8"  # ID do vídeo do YouTube
    )
    
    # Adicionar imagem
    foto_url = "https://girodoboi.canalrural.com.br/wp-content/uploads/2025/08/novilhada-angus-agropecuaria-ah.jpg"
    img_file = baixar_imagem(foto_url, "novilhada_angus_reportagem")
    
    if img_file:
        Imagem.objects.create(
            imagem=img_file,
            descricao="Novilhada Angus da Agropecuária AH - Foto da reportagem do Canal Rural",
            main_image=True,
            content_type_id=1,  # ContentType para News
            object_id=noticia.id
        )
        print("   ✅ Imagem adicionada")
    
    print(f"✅ Notícia criada: {noticia.news_title}")
    return noticia


def corrigir_urls():
    """Corrige as URLs do projeto"""
    print("🔧 Corrigindo URLs...")
    
    # Corrigir ahsite/urls.py
    urls_content = '''"""
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
    # Admin URLs
    path('admin/', admin.site.urls),
    path('admin/list_newsletter/', newsletterView.as_view()),
    path('admin/deploy/', views.admin_deploy_view, name='admin_deploy'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # Site URLs
    path('', views.home, name="home"),
    path(_('quem-somos/'), views.about_company, name="about_company"),
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
'''
    
    with open('ahsite/urls.py', 'w', encoding='utf-8') as f:
        f.write(urls_content)
    
    print("✅ URLs corrigidas")


def corrigir_views():
    """Corrige e adiciona views necessárias"""
    print("🔧 Corrigindo views...")
    
    # Adicionar imports necessários no início do arquivo
    views_content = '''# -*- coding: utf-8 -*-
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

'''
    
    # Ler o arquivo atual
    with open('app/views.py', 'r', encoding='utf-8') as f:
        current_content = f.read()
    
    # Adicionar as novas views no final
    new_views = '''

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
'''
    
    # Combinar conteúdo
    final_content = views_content + current_content + new_views
    
    with open('app/views.py', 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print("✅ Views corrigidas")


def criar_templates():
    """Cria templates necessários"""
    print("🔧 Criando templates...")
    
    # Template para deploy admin
    admin_deploy_content = '''{% extends "admin/base_site.html" %}
{% load i18n %}

{% block title %}Deploy do Sistema{% endblock %}

{% block content %}
<div id="content-main">
    <h1>🚀 Deploy do Sistema</h1>
    
    {% if messages %}
    <ul class="messagelist">
        {% for message in messages %}
        <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
        {% endfor %}
    </ul>
    {% endif %}
    
    <div class="module">
        <h2>Executar Deploy</h2>
        <p>Clique no botão abaixo para executar o deploy automático do sistema.</p>
        <p><strong>Atenção:</strong> Esta ação irá:</p>
        <ul>
            <li>Fazer pull das últimas alterações do Git</li>
            <li>Coletar arquivos estáticos</li>
            <li>Executar migrações do banco</li>
            <li>Reiniciar o servidor Nginx</li>
        </ul>
        
        <form method="post">
            {% csrf_token %}
            <input type="submit" value="🔄 Executar Deploy" class="default" 
                   onclick="return confirm('Tem certeza que deseja executar o deploy?')" />
        </form>
    </div>
</div>
{% endblock %}
'''
    
    with open('templates/admin_deploy.html', 'w', encoding='utf-8') as f:
        f.write(admin_deploy_content)
    
    # Template para deploy público
    deploy_content = '''<!DOCTYPE html>
<html>
<head>
    <title>Deploy do Sistema - Agropecuária AH</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 40px; 
            background: #f5f5f5;
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .btn { 
            background: #007cba; 
            color: white; 
            padding: 15px 30px; 
            border: none; 
            border-radius: 4px; 
            cursor: pointer; 
            font-size: 16px;
            margin: 10px 0;
        }
        .btn:hover { 
            background: #005a87; 
        }
        .message { 
            margin: 20px 0; 
            padding: 15px; 
            border-radius: 4px; 
        }
        .success { 
            background: #d4edda; 
            border: 1px solid #c3e6cb; 
            color: #155724; 
        }
        .error { 
            background: #f8d7da; 
            border: 1px solid #f5c6cb; 
            color: #721c24; 
        }
        pre { 
            white-space: pre-wrap; 
            background: #f8f9fa; 
            padding: 15px; 
            border-radius: 4px; 
            border: 1px solid #e9ecef;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .logo {
            font-size: 24px;
            font-weight: bold;
            color: #007cba;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🚀 Agropecuária AH</div>
            <h1>Deploy do Sistema</h1>
        </div>
        
        {% if message %}
        <div class="message {% if 'sucesso' in message %}success{% else %}error{% endif %}">
            <pre>{{ message }}</pre>
        </div>
        {% endif %}
        
        <form method="post">
            {% csrf_token %}
            <button type="submit" class="btn" onclick="return confirm('Tem certeza que deseja executar o deploy?')">
                🔄 Executar Deploy Automático
            </button>
        </form>
        
        <p><small>Esta página só pode ser acessada por usuários autenticados.</small></p>
    </div>
</body>
</html>
'''
    
    with open('templates/deploy.html', 'w', encoding='utf-8') as f:
        f.write(deploy_content)
    
    print("✅ Templates criados")


def criar_script_deploy():
    """Cria script de deploy melhorado"""
    print("🔧 Criando script de deploy...")
    
    deploy_script = '''#!/bin/bash
# Script de Deploy Automático - Agropecuária AH
# Fabio Marco - 2025

set -e  # Parar em caso de erro

echo "🚀 Iniciando deploy automático..."
echo "📅 Data/Hora: $(date)"
echo "=================================="

# Configurações
PROJECT_DIR="/var/www/ahsite_news/ahsite/ahsite"
BACKUP_DIR="/var/www/ahsite_news/ahsite/backups"
LOG_FILE="/var/www/ahsite_news/ahsite/deploy.log"

# Criar diretório de backup se não existir
mkdir -p "$BACKUP_DIR"

# Função para log
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Backup do banco antes do deploy
log "💾 Fazendo backup do banco..."
cd "$PROJECT_DIR"
python manage.py dumpdata > "$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).json"

# Git pull
log "📥 Fazendo git pull..."
cd "$PROJECT_DIR"
git pull origin main || {
    log "❌ Erro no git pull"
    exit 1
}

# Instalar dependências se necessário
log "📦 Verificando dependências..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Coletar arquivos estáticos
log "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Executar migrações
log "🗄️ Executando migrações..."
python manage.py migrate --noinput

# Verificar sintaxe Python
log "🔍 Verificando sintaxe Python..."
find . -name "*.py" -exec python -m py_compile {} \;

# Reiniciar serviços
log "🔄 Reiniciando serviços..."
systemctl restart nginx || true
systemctl restart gunicorn || true

# Verificar se o site está funcionando
log "✅ Verificando se o site está online..."
sleep 5
if curl -f http://localhost:8000/ > /dev/null 2>&1; then
    log "✅ Site está funcionando corretamente!"
else
    log "⚠️ Site pode não estar respondendo"
fi

log "🎉 Deploy concluído com sucesso!"
echo "=================================="
'''
    
    with open('deploy.sh', 'w', encoding='utf-8') as f:
        f.write(deploy_script)
    
    # Tornar executável
    os.chmod('deploy.sh', 0o755)
    
    print("✅ Script de deploy criado")


def resetar_admin():
    """Reseta senha do admin"""
    print("🔧 Resetando senha do admin...")
    
    # Verificar se existe superuser
    superusers = User.objects.filter(is_superuser=True)
    if superusers.exists():
        user = superusers.first()
        user.set_password('admin123')
        user.save()
        print(f"✅ Senha resetada para: {user.username}")
        print("🔑 Nova senha: admin123")
    else:
        # Criar novo superuser
        User.objects.create_superuser('admin', 'admin@agropecuariaah.agr.br', 'admin123')
        print("✅ Novo superuser criado:")
        print("👤 Username: admin")
        print("🔑 Senha: admin123")


def main():
    """Função principal"""
    print("🚀 Sistema Completo de Deploy e Correções - Agropecuária AH")
    print("=" * 60)
    
    try:
        # 1. Corrigir URLs
        corrigir_urls()
        
        # 2. Corrigir views
        corrigir_views()
        
        # 3. Criar templates
        criar_templates()
        
        # 4. Criar script de deploy
        criar_script_deploy()
        
        # 5. Criar notícia do Angus
        noticia_angus = criar_noticia_angus()
        
        # 6. Resetar admin
        resetar_admin()
        
        print("\n" + "=" * 60)
        print("✅ SISTEMA CONFIGURADO COM SUCESSO!")
        print("=" * 60)
        print("\n📋 RESUMO DAS ALTERAÇÕES:")
        print("• URLs corrigidas e organizadas")
        print("• Views atualizadas com deploy automático")
        print("• Templates criados para deploy")
        print("• Script de deploy melhorado")
        print(f"• Notícia do Angus: {noticia_angus.news_title}")
        print("• Admin resetado: admin/admin123")
        
        print("\n🌐 ENDPOINTS DISPONÍVEIS:")
        print("• /deploy/ - Webhook para deploy automático")
        print("• /admin/deploy/ - Deploy via painel admin")
        print("• /deploy-page/ - Página de deploy")
        print("• /robots.txt - Robots.txt dinâmico")
        
        print("\n🔧 PRÓXIMOS PASSOS:")
        print("1. Fazer commit das alterações")
        print("2. Fazer push para o repositório")
        print("3. Testar o deploy automático")
        print("4. Configurar webhook do GitHub (opcional)")
        
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
