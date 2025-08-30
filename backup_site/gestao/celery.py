import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')

app = Celery('ahsite')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from .celery import app as celery_app

__all__ = ('celery_app',)