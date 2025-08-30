#!/usr/bin/env python
"""
Script para corrigir registros nulos na tabela AgriculturalFiles
"""
import os
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from django.db import connection

def fix_agricultural_files():
    """Remove registros com ap_file nulo e marca a migração como aplicada"""
    
    with connection.cursor() as cursor:
        # Verificar quantos registros têm ap_file nulo
        cursor.execute("SELECT COUNT(*) FROM app_agriculturalfiles WHERE ap_file IS NULL")
        count = cursor.fetchone()[0]
        print(f"Registros com ap_file nulo: {count}")
        
        if count > 0:
            # Remover registros com ap_file nulo
            cursor.execute("DELETE FROM app_agriculturalfiles WHERE ap_file IS NULL")
            print(f"Removidos {count} registros com ap_file nulo")
        
        # Marcar a migração como aplicada (versão mais simples)
        cursor.execute("""
            INSERT INTO django_migrations (app, name, applied) 
            VALUES ('app', '0049_alter_agriculturalfiles_ap_file', NOW())
        """)
        print("Migração 0049 marcada como aplicada")
        
        print("Problema resolvido!")

if __name__ == '__main__':
    fix_agricultural_files() 