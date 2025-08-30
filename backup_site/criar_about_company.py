#!/usr/bin/env python
import os
import sys
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from app.models import AboutCompany

def criar_about_company():
    """Cria um registro inicial na tabela AboutCompany"""
    
    # Verificar se já existe algum registro
    if AboutCompany.objects.exists():
        print("Já existe pelo menos um registro na tabela AboutCompany.")
        return
    
    # Criar um registro inicial
    about = AboutCompany.objects.create(
        ac_content="<p><strong>Sobre a Agropecuária AH</strong></p><p>A Agropecuária AH é uma empresa líder no setor agropecuário, comprometida com a excelência e inovação. Nossa missão é fornecer produtos e serviços de alta qualidade para o desenvolvimento sustentável da agricultura e pecuária.</p><p><strong>Nossa Missão:</strong> Contribuir para o crescimento e modernização do setor agropecuário através de soluções inovadoras e sustentáveis.</p><p><strong>Nossa Visão:</strong> Ser referência nacional em excelência e inovação no setor agropecuário.</p>",
        language="pt"
    )
    
    print(f"Registro AboutCompany criado com sucesso! ID: {about.id}")
    print(f"Idioma: {about.language}")
    print(f"Conteúdo: {about.ac_content[:100]}...")

if __name__ == "__main__":
    criar_about_company() 