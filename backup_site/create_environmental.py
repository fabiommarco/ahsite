import os
import django
from django.utils import timezone

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from app.models import EnvironmentalResponsability

# Criar um registro padrão de responsabilidade ambiental
environmental = EnvironmentalResponsability(
    environ_date=timezone.now(),
    environ_title="Responsabilidade Ambiental",
    environ_description="""
    <p>A Agropecuária AH tem como um de seus principais valores a responsabilidade ambiental. 
    Nossas ações são pautadas pelo desenvolvimento sustentável, buscando sempre o equilíbrio 
    entre produção e preservação do meio ambiente.</p>
    
    <p>Entre nossas principais iniciativas ambientais estão:</p>
    
    <ul>
        <li>Gestão sustentável dos recursos naturais</li>
        <li>Preservação de áreas de mata nativa</li>
        <li>Tratamento adequado de resíduos</li>
        <li>Uso eficiente de água e energia</li>
        <li>Programas de educação ambiental</li>
    </ul>
    
    <p>Estamos comprometidos em reduzir nosso impacto ambiental e contribuir para um futuro 
    mais sustentável para as próximas gerações.</p>
    """,
    language='pt'
)

# Salvar o registro
environmental.save()

print("Registro de responsabilidade ambiental criado com sucesso!") 