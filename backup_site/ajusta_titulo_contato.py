#!/usr/bin/env python
import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from app.models import Sale

def ajusta_titulo_contato():
    sale = Sale.objects.first()
    if sale:
        conteudo = sale.sale_description
        # Garante que o h3 do contato fique com a classe text-success
        conteudo_novo = re.sub(
            r'<h3[^>]*>[\s\n]*Entre em Contato com nossa equipe:.*?</h3>',
            r'<h3 class="text-success">Entre em Contato com nossa equipe:</h3>',
            conteudo,
            flags=re.DOTALL | re.IGNORECASE
        )
        sale.sale_description = conteudo_novo
        sale.save()
        print("Título ajustado para verde!")
    else:
        print("Nenhum registro encontrado na tabela Sale.")

if __name__ == "__main__":
    ajusta_titulo_contato() 