#!/usr/bin/env python
"""
Script para verificar e corrigir imagens das notícias
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from app.models import News, Imagem
from django.contrib.contenttypes.models import ContentType

def verificar_imagens_noticias():
    """Verifica e corrige imagens das notícias"""
    print("🔍 Verificando imagens das notícias...")
    
    # Obter ContentType para News
    news_ct = ContentType.objects.get_for_model(News)
    
    # Verificar notícias
    noticias = News.objects.all()
    print(f"📰 Total de notícias: {noticias.count()}")
    
    for noticia in noticias:
        print(f"\n📄 Notícia: {noticia.news_title}")
        
        # Verificar imagens associadas
        imagens = Imagem.objects.filter(
            content_type=news_ct,
            object_id=noticia.id
        )
        
        print(f"   🖼️ Imagens encontradas: {imagens.count()}")
        
        if imagens.count() == 0:
            print(f"   ⚠️ Nenhuma imagem associada!")
            
            # Verificar se há imagens no diretório que podem ser associadas
            if noticia.news_slug == '15a-cavalgada-ah':
                # Associar a imagem angus_1.jpg à notícia da cavalgada
                try:
                    imagem = Imagem.objects.create(
                        imagem='news_images/angus_1.jpg',
                        descricao='Cavalgada AH',
                        main_image=True,
                        content_type=news_ct,
                        object_id=noticia.id
                    )
                    print(f"   ✅ Imagem associada: {imagem.imagem}")
                except Exception as e:
                    print(f"   ❌ Erro ao associar imagem: {e}")
        else:
            for img in imagens:
                print(f"   ✅ Imagem: {img.imagem} - Principal: {img.main_image}")

def verificar_produtos():
    """Verifica produtos e suas imagens"""
    print("\n🔍 Verificando produtos...")
    
    from app.models import Products
    products_ct = ContentType.objects.get_for_model(Products)
    
    produtos = Products.objects.all()
    print(f"📦 Total de produtos: {produtos.count()}")
    
    for produto in produtos:
        print(f"\n📦 Produto: {produto.product_name}")
        
        imagens = Imagem.objects.filter(
            content_type=products_ct,
            object_id=produto.id
        )
        
        print(f"   🖼️ Imagens encontradas: {imagens.count()}")
        
        if imagens.count() == 0:
            print(f"   ⚠️ Nenhuma imagem associada!")

if __name__ == '__main__':
    verificar_imagens_noticias()
    verificar_produtos()
    print("\n✅ Verificação concluída!")
