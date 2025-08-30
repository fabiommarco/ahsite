#!/usr/bin/env python3
"""
Script para criar banners no banco de dados
"""

import os
import sys
import django
from datetime import datetime

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from app.models import Banner

def criar_banners():
    """Cria banners padrão para o site"""
    
    banners_data = [
        {
            'titulo': 'Agropecuária AH - Excelência em Pecuária',
            'descricao': 'Especialistas em criação de gado de corte com foco em qualidade e produtividade',
            'imagem': 'banner1.jpg',
            'link': '/',
            'ativo': True,
            'ordem': 1
        },
        {
            'titulo': 'Melhoramento Genético de Qualidade',
            'descricao': 'Trabalhamos com as melhores linhagens para garantir resultados superiores',
            'imagem': 'banner2.jpg',
            'link': '/produtos/',
            'ativo': True,
            'ordem': 2
        },
        {
            'titulo': 'Sustentabilidade e Inovação',
            'descricao': 'Compromisso com o meio ambiente e tecnologias avançadas',
            'imagem': 'banner3.jpg',
            'link': '/sobre/',
            'ativo': True,
            'ordem': 3
        }
    ]
    
    banners_criados = []
    
    for banner_data in banners_data:
        try:
            # Verificar se já existe um banner com esta ordem
            if Banner.objects.filter(ordem=banner_data['ordem']).exists():
                print(f"⚠️ Banner com ordem {banner_data['ordem']} já existe, pulando...")
                continue
            
            # Criar o banner
            banner = Banner(
                titulo=banner_data['titulo'],
                descricao=banner_data['descricao'],
                imagem=banner_data['imagem'],
                link=banner_data['link'],
                ativo=banner_data['ativo'],
                ordem=banner_data['ordem'],
                data_criacao=datetime.now(),
                data_atualizacao=datetime.now()
            )
            banner.save()
            
            banners_criados.append(banner)
            print(f"✅ Banner criado: {banner.titulo}")
            
        except Exception as e:
            print(f"❌ Erro ao criar banner: {e}")
    
    return banners_criados

if __name__ == "__main__":
    print("🚀 Criando banners para o site...")
    banners = criar_banners()
    
    if banners:
        print(f"\n🎉 {len(banners)} banners criados com sucesso!")
        print("🌐 Acesse: http://127.0.0.1:8000/ para ver o site")
    else:
        print("\n❌ Nenhum banner foi criado")
        sys.exit(1)
