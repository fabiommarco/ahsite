#!/usr/bin/env python3
"""
Script para adicionar fotos da 9ª Festa do Café
"""

import os
import sys
import django
import shutil
from django.core.files import File
from pathlib import Path

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from app.models import News, Imagem
from django.contrib.contenttypes.models import ContentType

def adicionar_fotos_festa_cafe():
    """Adiciona fotos da 9a Festa do Cafe a noticia"""
    
    print("Adicionando fotos da 9a Festa do Cafe...")
    
    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
    django.setup()
    
    from app.models import News, Imagem
    
    # Buscar a noticia da 9a Festa do Cafe
    noticia_cafe = News.objects.filter(news_title__icontains="9a Festa do Cafe").first()
    
    if not noticia_cafe:
        print("Noticia da 9a Festa do Cafe nao encontrada")
        return False
    
    print(f"Noticia encontrada: {noticia_cafe.news_title}")
    
    # Listar arquivos de imagem na pasta
    extensoes_imagem = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    fotos_encontradas = []
    
    for arquivo in os.listdir(pasta_fotos):
        if any(arquivo.lower().endswith(ext) for ext in extensoes_imagem):
            fotos_encontradas.append(arquivo)
    
    print(f"Encontradas {len(fotos_encontradas)} fotos na pasta:")
    for foto in fotos_encontradas:
        print(f"   - {foto}")
    
    if not fotos_encontradas:
        print("Nenhuma foto encontrada na pasta")
        return False
    
    # Remover imagens existentes da notícia
    if noticia_cafe.news_galery.exists():
        print("   ⚠️ Removendo imagens existentes...")
        noticia_cafe.news_galery.all().delete()
    
    # Adicionar as fotos
    content_type = ContentType.objects.get_for_model(News)
    fotos_adicionadas = 0
    
    for i, foto in enumerate(fotos_encontradas):
        caminho_foto = os.path.join(pasta_fotos, foto)
        
        try:
            # Abrir o arquivo
            with open(caminho_foto, 'rb') as f:
                # Criar nome único para o arquivo
                nome_arquivo = f"festa_cafe_{i+1}_{foto}"
                
                # Criar o registro de imagem
                imagem = Imagem.objects.create(
                    imagem=File(f, name=nome_arquivo),
                    descricao=f"9ª Festa do Café da Fazenda Ouro Verde - {foto}",
                    main_image=(i == 0),  # Primeira foto como principal
                    content_type=content_type,
                    object_id=noticia_cafe.id
                )
                
                print(f"   ✅ Foto adicionada: {foto}")
                fotos_adicionadas += 1
                
        except Exception as e:
            print(f"   ❌ Erro ao adicionar {foto}: {e}")
    
    print()
    print("✅ Processo concluído!")
    print(f"Total de fotos adicionadas: {fotos_adicionadas}")
    
    # Verificar resultado
    total_imagens = noticia_cafe.news_galery.count()
    print(f"Total de imagens na notícia: {total_imagens}")
    
    if total_imagens > 0:
        print("Fotos da 9ª Festa do Café adicionadas com sucesso!")
        print("Acesse a notícia para ver as fotos: http://127.0.0.1:8000/noticias/9a-festa-do-cafe-da-fazenda-ouro-verde")
    else:
        print("Nenhuma foto foi adicionada")

if __name__ == "__main__":
    adicionar_fotos_festa_cafe()
