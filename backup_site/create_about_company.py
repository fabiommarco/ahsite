import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from app.models import AboutCompany

conteudo = '''<p>Bem-vindo à Agropecuária AH!<br>
Nossa empresa atua com excelência no setor agropecuário, prezando pela inovação, sustentabilidade e compromisso com a qualidade.<br>
Esta é uma página institucional padrão. Edite este conteúdo pelo painel administrativo para personalizar as informações da sua empresa.</p>'''

about = AboutCompany(
    ac_content=conteudo,
    gallery_title="Galeria de Imagens",
    language='pt'
)
about.save()
print("Registro padrão de 'Quem Somos' criado com sucesso!") 