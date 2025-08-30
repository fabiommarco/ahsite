import os
import sys
import django

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from app.models import Products

print("🔍 Verificando produtos...")

produtos = Products.objects.all()
print(f"📦 Total de produtos: {produtos.count()}")

for produto in produtos:
    print(f"📦 {produto.product_name} - Categoria: {produto.product_category} - Idioma: {produto.language}")

print("\n✅ Verificação concluída!")
