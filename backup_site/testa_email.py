import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from django.core.mail import send_mail

try:
    send_mail(
        'Teste de envio',
        'Este é um teste de envio de e-mail pelo Django.',
        'ti@ah.agr.br',  # Remetente
        ['ti@ah.agr.br'],  # Destinatário (pode trocar para outro e-mail seu)
        fail_silently=False,
    )
    print('Enviado com sucesso!')
except Exception as e:
    print('Erro ao enviar e-mail:')
    print(e) 