from django.db import models
from django.contrib import admin

# Create your models here.

class Backup(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='backups/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Backup em {self.created_at.strftime('%d/%m/%Y %H:%M:%S')}"

class Update(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='updates/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Update em {self.uploaded_at.strftime('%d/%m/%Y %H:%M:%S')}"

class BackupConfig(models.Model):
    agendar_backup = models.BooleanField(default=False, verbose_name="Agendar backup automático?")
    horario = models.TimeField(default='02:00', verbose_name="Horário do backup (HH:MM)")

    def __str__(self):
        return "Configuração de Backup"

admin.site.register(BackupConfig)
