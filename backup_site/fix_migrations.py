import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

def fix_migrations():
    with connection.cursor() as cursor:
        # Deletar todas as entradas da tabela django_migrations
        cursor.execute("DELETE FROM django_migrations;")
        
        # Resetar a sequência
        cursor.execute("ALTER SEQUENCE django_migrations_id_seq RESTART WITH 1;")
        
        print("Tabela de migrações limpa e sequência resetada.")
        print("Agora execute:")
        print("python manage.py migrate --fake")

if __name__ == '__main__':
    fix_migrations() 