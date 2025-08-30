#!/usr/bin/env python3
"""
Script para criar a notícia sobre a 9ª Festa do Café da Fazenda Ouro Verde
"""

import os
import sys
import django
from datetime import datetime
from django.utils.text import slugify

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from app.models import News

def criar_noticia_cafe():
    """Cria a notícia sobre a 9ª Festa do Café da Fazenda Ouro Verde"""

    # Dados da notícia
    titulo = "9ª Festa do Café da Fazenda Ouro Verde"
    
    # Gerar slug único com timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    slug_base = slugify(titulo)
    slug = f"{slug_base}-{timestamp}"
    
    # Verificar se já existe uma notícia com este slug
    counter = 1
    while News.objects.filter(news_slug=slug).exists():
        slug = f"{slug_base}-{timestamp}-{counter}"
        counter += 1

    # Conteúdo da notícia
    conteudo = """
    <h2>9ª Festa do Café da Fazenda Ouro Verde: Renovação e Celebração</h2>

    <p>No último dia <strong>16 de Agosto</strong> celebramos, na fazenda Ouro Verde, nossa <strong>9ª Festa do Café</strong>. Com ela, renovamos nossas energias, encerramos um ciclo e já iniciamos outro.</p>

    <h3>Um Momento de Conquistas e Reflexão</h3>
    <p>Regada a muita comida, música e diversão, celebramos nossas conquistas. No ano em que a fazenda Ouro Verde completa 10 anos, aproveitamos esse momento para refletir: nada na fazenda funciona por si só, mas é sempre o resultado de interações complexas entre os elementos naturais solo, plantas, animais e seres humanos. Todos estes elementos são partes integrantes da fazenda e devem ser geridos juntos para garantir o bem estar do todo, formando o organismo agrícola.</p>

    <h3>Reconhecimento e Propósito</h3>
    <p>Com esse espírito, também realizamos nessa oportunidade a premiação por tempo de serviço aos nossos trabalhadores, que dedicam parte de sua vida para que nossa empresa e nosso país caminhem para frente.</p>
    <p>Agradecemos a todos envolvidos e seguimos em busca de nosso propósito: desfrutamos de sistemas de produção rentáveis que promovem a regeneração do solo e a qualidade de vida das pessoas.</p>
    """

    try:
        # Criar a notícia
        noticia = News(
            news_date=datetime.now(),
            news_title=titulo,
            news_slug=slug,
            news_description=conteudo,
            news_video="",  # Campo opcional
            news_galery_title="Galeria de Imagens da Festa do Café"
        )
        noticia.save()

        print("Noticia criada com sucesso!")
        print("Titulo: {}".format(noticia.news_title))
        print("Slug: {}".format(noticia.news_slug))
        print("Data: {}".format(noticia.news_date))
        print("ID: {}".format(noticia.id))

        return noticia

    except Exception as e:
        print("Erro ao criar noticia: {}".format(e))
        return None

if __name__ == "__main__":
    print("Criando noticia sobre a 9a Festa do Cafe da Fazenda Ouro Verde...")
    noticia = criar_noticia_cafe()

    if noticia:
        print("\nNoticia criada com sucesso!")
        print("Acesse: http://127.0.0.1:8000/ para ver o site")
        print("Admin: http://127.0.0.1:8000/admin/ para gerenciar conteudo")
    else:
        print("\nFalha ao criar a noticia")
        sys.exit(1)
