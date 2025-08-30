#!/usr/bin/env python
"""
Script para corrigir o banco de dados criando tabelas que estão faltando
"""
import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line
from app.models import AgriculturalFiles

def create_missing_tables():
    """Cria as tabelas que estão faltando no banco de dados"""
    
    # Lista de tabelas que devem existir
    required_tables = [
        'app_aboutcompany',
        'app_event', 
        'app_environmentalresponsability',
        'app_news',
        'app_partners',
        'app_products',
        'app_jobs',
        'app_farm',
        'app_magazine',
        'app_research',
        'app_newsletter',
        'app_sale',
        'app_agriculturalfiles',
        'app_timeline',
        'app_imagem',
        'app_attachment',
        'app_generalconfig'
    ]
    
    with connection.cursor() as cursor:
        # Verificar quais tabelas existem
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name LIKE 'app_%'
        """)
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        print("Tabelas existentes:", existing_tables)
        print("Tabelas necessárias:", required_tables)
        
        missing_tables = [table for table in required_tables if table not in existing_tables]
        
        if missing_tables:
            print(f"\nTabelas faltando: {missing_tables}")
            print("Criando tabelas faltando...")
            
            # Executar makemigrations e migrate para criar as tabelas
            execute_from_command_line(['manage.py', 'makemigrations', 'app'])
            execute_from_command_line(['manage.py', 'migrate', 'app'])
            
            print("Tabelas criadas com sucesso!")
        else:
            print("Todas as tabelas necessárias já existem!")

if __name__ == '__main__':
    create_missing_tables()
    AgriculturalFiles.objects.filter(ap_file__isnull=True).delete() 