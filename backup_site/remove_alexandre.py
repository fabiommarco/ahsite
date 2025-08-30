#!/usr/bin/env python
import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from app.models import Sale

def remove_alexandre():
    sale = Sale.objects.first()
    if sale:
        conteudo = sale.sale_description
        # Remove o bloco do Alexandre Brazoloto (nome, telefone e e-mail)
        conteudo_novo = re.sub(
            r"<p>Alexandre Brazoloto.*?ah\.agr\.br.*?</p>", "", conteudo, flags=re.DOTALL | re.IGNORECASE
        )
        # Deixar o h3 Entre em Contato com nossa equipe: com a classe text-success
        conteudo_novo = re.sub(
            r"<h3>(\s*Entre em Contato com nossa equipe:.*?</h3>)",
            r'<h3 class="text-success">\1',
            conteudo_novo,
            flags=re.DOTALL | re.IGNORECASE
        )
        sale.sale_description = conteudo_novo
        sale.save()
        print("Bloco do Alexandre Brazoloto removido e título ajustado!")
    else:
        print("Nenhum registro encontrado na tabela Sale.")

if __name__ == "__main__":
    remove_alexandre() 