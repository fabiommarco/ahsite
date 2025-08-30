#!/usr/bin/env python3
"""
Script para adicionar imagens às notícias que criamos
"""

import os
import sys
import django
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from app.models import News, Imagem
from django.contrib.contenttypes.models import ContentType

def adicionar_imagens_noticias():
    """Adiciona imagens às notícias que criamos"""
    
    print("🖼️ Adicionando imagens às notícias...")
    print("=" * 50)
    
    # Buscar nossas notícias específicas
    noticia_cafe = News.objects.filter(news_title__icontains="9ª Festa do Café").first()
    noticia_angus = News.objects.filter(news_title__icontains="Novilhada Angus").first()
    
    # URLs de imagens de exemplo (você pode substituir por URLs reais)
    imagem_cafe_url = "https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=800&h=600&fit=crop"
    imagem_angus_url = "https://images.unsplash.com/photo-1500595046743-cd271d694e30?w=800&h=600&fit=crop"
    
    def baixar_imagem(url, nome_arquivo):
        """Baixa uma imagem da URL e retorna um arquivo temporário"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Criar arquivo temporário
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(response.content)
            img_temp.flush()
            
            return File(img_temp, name=f"{nome_arquivo}.jpg")
        except Exception as e:
            print(f"❌ Erro ao baixar imagem: {e}")
            return None
    
    # Adicionar imagem à notícia do café
    if noticia_cafe:
        print(f"📰 Adicionando imagem à notícia do Café...")
        
        # Verificar se já tem imagem
        if noticia_cafe.news_galery.exists():
            print("   ⚠️ Notícia já tem imagem, removendo...")
            noticia_cafe.news_galery.all().delete()
        
        # Baixar e adicionar imagem
        img_file = baixar_imagem(imagem_cafe_url, "festa_cafe")
        if img_file:
            content_type = ContentType.objects.get_for_model(News)
            imagem = Imagem.objects.create(
                imagem=img_file,
                descricao="9ª Festa do Café da Fazenda Ouro Verde",
                main_image=True,
                content_type=content_type,
                object_id=noticia_cafe.id
            )
            print(f"   ✅ Imagem adicionada: {imagem.imagem.name}")
        else:
            print("   ❌ Falha ao adicionar imagem")
    else:
        print("❌ Notícia do Café não encontrada")
    
    print()
    
    # Adicionar imagem à notícia do Angus
    if noticia_angus:
        print(f"📰 Adicionando imagem à notícia do Angus...")
        
        # Verificar se já tem imagem
        if noticia_angus.news_galery.exists():
            print("   ⚠️ Notícia já tem imagem, removendo...")
            noticia_angus.news_galery.all().delete()
        
        # Baixar e adicionar imagem
        img_file = baixar_imagem(imagem_angus_url, "novilhada_angus")
        if img_file:
            content_type = ContentType.objects.get_for_model(News)
            imagem = Imagem.objects.create(
                imagem=img_file,
                descricao="Novilhada Angus da Agropecuária AH",
                main_image=True,
                content_type=content_type,
                object_id=noticia_angus.id
            )
            print(f"   ✅ Imagem adicionada: {imagem.imagem.name}")
        else:
            print("   ❌ Falha ao adicionar imagem")
    else:
        print("❌ Notícia do Angus não encontrada")
    
    print()
    print("✅ Processo concluído!")
    print()
    print("🔍 Verificando imagens das notícias:")
    print("-" * 50)
    
    if noticia_cafe:
        print(f"Café: {noticia_cafe.news_galery.count()} imagem(s)")
        for img in noticia_cafe.news_galery.all():
            print(f"   - {img.imagem.name}")
    
    if noticia_angus:
        print(f"Angus: {noticia_angus.news_galery.count()} imagem(s)")
        for img in noticia_angus.news_galery.all():
            print(f"   - {img.imagem.name}")

if __name__ == "__main__":
    adicionar_imagens_noticias()
