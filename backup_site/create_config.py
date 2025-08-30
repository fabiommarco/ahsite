import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from app.models import GeneralConfig

# Criar objeto GeneralConfig com valores padrão
config = GeneralConfig(
    config_street="Rua Exemplo",
    config_number=123,
    config_neighbourhood="Centro",
    config_email="contato@exemplo.com",
    config_phone="(18) 1234-5678"
)
config.save()

print("Configuração geral criada com sucesso!") 