import os
import shutil
import sqlite3

# Remover arquivos .pyc e __pycache__
migrations_dir = os.path.join('app', 'migrations')
for file in os.listdir(migrations_dir):
    if file.endswith('.pyc'):
        os.remove(os.path.join(migrations_dir, file))
    elif file == '__pycache__':
        shutil.rmtree(os.path.join(migrations_dir, file))

# Remover banco de dados
if os.path.exists('db.sqlite3'):
    os.remove('db.sqlite3')

print("Limpeza concluída. Agora execute:")
print("python manage.py makemigrations")
print("python manage.py migrate") 