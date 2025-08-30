import os
import django
import csv
from datetime import datetime
import re
from django.utils import timezone
from django.utils.text import slugify
import uuid

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from app.models import News

def parse_date(date_str):
    # Remove o fuso horário (-03 ou -02)
    date_str = re.sub(r'-\d{2}$', '', date_str)
    # Converte para datetime e adiciona o fuso horário
    dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    return timezone.make_aware(dt)

def generate_unique_slug(title):
    base_slug = slugify(title)
    unique_slug = f"{base_slug}-{str(uuid.uuid4())[:8]}"
    return unique_slug

# Limpar todas as notícias existentes
News.objects.all().delete()

# Ler o arquivo CSV
with open('C:/backup_ah/backup_base/news.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            # Criar uma nova notícia
            news = News(
                news_date=parse_date(row['news_date']),
                news_title=row['news_title'],
                news_description=f"<div style=\"font-size:22px;\">{row['news_description']}</div>",
                news_video=row['news_video'] if row['news_video'] else '',
                news_galery_title=row['news_galery_title'] if row['news_galery_title'] else '',
                language='pt'
            )
            # Gerar slug único antes de salvar
            news.news_slug = generate_unique_slug(row['news_title'])
            news.save()
            print(f"Notícia importada: {news.news_title}")
        except Exception as e:
            print(f"Erro ao importar notícia {row.get('news_title', 'N/A')}: {str(e)}")

print("Importação concluída!") 