#!/usr/bin/env python
import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from app.models import AboutCompany

def adiciona_classe_titulos():
    about = AboutCompany.objects.first()
    if about:
        conteudo = about.ac_content
        # Adiciona a classe nos h2 e h3 (mantendo ids)
        conteudo = re.sub(r'<h2(.*?)>', r'<h2\1 class="titulo-institucional">', conteudo)
        conteudo = re.sub(r'<h3(.*?)>', r'<h3\1 class="titulo-institucional">', conteudo)
        about.ac_content = conteudo
        about.save()
        print('Classe adicionada em todos os títulos!')
    else:
        print('Nenhum registro encontrado na tabela AboutCompany.')

if __name__ == "__main__":
    adiciona_classe_titulos() 