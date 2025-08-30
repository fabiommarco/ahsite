#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para criar notícia usando SQLite temporariamente
"""

import os
import sys
import django
from datetime import datetime

# Configurar o Django para usar SQLite temporariamente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')

# Modificar as configurações do banco antes de inicializar o Django
import django.conf
from django.conf import settings

# Configurar SQLite temporariamente
settings.DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

try:
    django.setup()
    from app.models import News
    
    def criar_noticia_angus():
        """Cria notícia sobre a novilhada Angus da Agropecuária AH"""
        
        # Dados da notícia baseados no link fornecido
        titulo = "Novilhada Angus da Agropecuária AH surpreende com ganho de 1 arroba por mês"
        
        descricao = """
        <h2>Novilhada Angus impressiona com 17,5 arrobas aos 17 meses</h2>
        
        <p>A <strong>Agropecuária AH</strong>, através da <strong>Fazenda Córrego Azul</strong> em <strong>Brasilândia (MS)</strong>, está chamando atenção no setor pecuário com resultados excepcionais em sua criação de novilhas Angus.</p>
        
        <h3>Resultados Impressionantes</h3>
        
        <p>O pecuarista <strong>Helder Hofig</strong> e sua equipe conseguiram um feito notável: suas novilhas Angus estão ganhando <strong>uma arroba por mês</strong>, alcançando <strong>17,5 arrobas aos 17 meses de idade</strong>.</p>
        
        <p>Esses resultados foram apresentados pelo <strong>Alexandre Scaff Raffi</strong>, gerente da unidade CPG da Friboi de Campo Grande (MS), que destacou a qualidade excepcional do lote de novilhas Angus crioulas da fazenda.</p>
        
        <h3>Sistema de Produção</h3>
        
        <p>O sucesso é resultado de um sistema integrado que inclui:</p>
        
        <ul>
            <li><strong>Melhoramento genético intra-rebanho</strong> com acompanhamento do professor doutor José Bento Ferraz da USP de Pirassununga</li>
            <li><strong>Pastoreio Racional Voisin</strong> para a fase de cria</li>
            <li><strong>Confinamento</strong> para terminação</li>
            <li>Aprovação no <strong>Protocolo 1953</strong> da Friboi</li>
        </ul>
        
        <h3>Protocolo 1953</h3>
        
        <p>O Protocolo 1953, lançado em 2018, privilegia pecuaristas que trabalham para obter animais que garantem carne macia, saborosa e suculenta. Entre os requisitos estão:</p>
        
        <ul>
            <li>Mínimo de 50% de sangue de raças taurinas</li>
            <li>Machos castrados com até dois dentes incisivos</li>
            <li>Novilhas com até quatro dentes</li>
            <li>Maturidade e acabamento adequados</li>
        </ul>
        
        <h3>Reconhecimento da Qualidade</h3>
        
        <p>Essa novilhada representa o que há de mais moderno na pecuária brasileira, demonstrando que investimento em genética, manejo adequado e tecnologia podem resultar em produtos de altíssima qualidade, valorizando tanto o produtor quanto o consumidor final.</p>
        
        <p>A <strong>Agropecuária AH</strong> continua se destacando como referência em pecuária de precisão e qualidade no Mato Grosso do Sul.</p>
        """
        
        # Criar a notícia
        try:
            noticia = News.objects.create(
                news_date=datetime.now(),
                news_title=titulo,
                news_description=descricao,
                language='pt'
            )
            
            print(f"✅ Notícia criada com sucesso!")
            print(f"📰 ID: {noticia.id}")
            print(f"📰 Título: {noticia.news_title}")
            print(f"🔗 Slug: {noticia.news_slug}")
            print(f"📅 Data: {noticia.news_date}")
            print(f"🌐 Idioma: {noticia.language}")
            
            return noticia
            
        except Exception as e:
            print(f"❌ Erro ao criar notícia: {e}")
            return None

    if __name__ == "__main__":
        print("🚀 Criando notícia sobre novilhada Angus da Agropecuária AH...")
        print("📝 Baseado nas informações do Giro do Boi")
        print("🔗 Fonte: https://girodoboi.canalrural.com.br/pecuaria/certificacoes-e-qualidade/novilhada-angus-surpreende-por-ganhar-1-arroba-por-mes-175-arrobas-aos-17-meses")
        print()
        
        noticia = criar_noticia_angus()
        
        if noticia:
            print("\n🎉 Notícia criada com sucesso no sistema!")
            print("📝 A notícia está disponível no banco de dados SQLite.")
            print("💡 Para visualizar, acesse o painel administrativo do Django.")
        else:
            print("\n💥 Falha ao criar a notícia.")
            sys.exit(1)

except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("💡 Verifique se todas as dependências estão instaladas")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    sys.exit(1)
