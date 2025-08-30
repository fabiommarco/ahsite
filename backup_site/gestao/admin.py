from django.contrib import admin
from .models import Backup, Update
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.conf import settings
import os
import subprocess
from gestao.tasks import backup_task, backup_completo_task
import datetime

__all__ = ('celery_app',)

@admin.register(Backup)
class BackupAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'file', 'description', 'download_link')
    search_fields = ('description',)
    list_filter = ('created_at',)
    actions = ['criar_backup', 'restaurar_backup', 'backup_completo', 'deletar_backups']
    readonly_fields = ('created_at', 'file', 'description', 'instrucoes')
    fieldsets = (
        ('Instruções', {
            'fields': ('instrucoes',),
            'description': 'Leia atentamente antes de realizar qualquer ação de backup ou restauração.'
        }),
        ('Informações do Backup', {
            'fields': ('file', 'description', 'created_at'),
        }),
    )

    def instrucoes(self, obj=None):
        return mark_safe('<b>Backup:</b> Gere um backup do banco de dados atual. <br>'
                         '<b>Restauração:</b> Selecione um backup e use a ação para restaurar. <br>'
                         '<span style="color:#d9534f;">Atenção: a restauração sobrescreve os dados atuais!</span>')
    instrucoes.short_description = 'Instruções'

    def criar_backup(self, request, queryset):
        backup_name = f"backup_{timezone.now().strftime('%Y-%m-%d_%H-%M-%S')}.dump"
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        backup_path = os.path.join(backup_dir, backup_name)
        task = backup_task.delay(backup_path)
        self.message_user(request, f"Backup iniciado. Aguarde o processo ser concluído. Task ID: {task.id}")
    criar_backup.short_description = 'Gerar novo backup do banco de dados'

    def restaurar_backup(self, request, queryset):
        for backup in queryset:
            cmd = f"pg_restore -U postgres -d ah --clean '{backup.file.path}'"
            result = subprocess.run(cmd, shell=True)
            if result.returncode == 0:
                self.message_user(request, f"Backup restaurado: {backup.file.name}")
            else:
                self.message_user(request, f"Erro ao restaurar: {backup.file.name}", level='error')
            break
    restaurar_backup.short_description = 'Restaurar banco a partir do backup selecionado'

    def backup_completo(self, request, queryset):
        task = backup_completo_task.delay()
        self.message_user(request, f"Backup completo (banco + media) iniciado. Aguarde o processo ser concluído. Task ID: {task.id}")
    backup_completo.short_description = 'Gerar backup completo (banco + media)'

    def deletar_backups(self, request, queryset):
        count = 0
        for backup in queryset:
            try:
                # Deletar arquivo físico se existir
                if backup.file and os.path.exists(backup.file.path):
                    os.remove(backup.file.path)
                # Deletar registro do banco
                backup.delete()
                count += 1
            except Exception as e:
                self.message_user(request, f"Erro ao deletar {backup.file.name}: {str(e)}", level='error')
        
        if count > 0:
            self.message_user(request, f"{count} backup(s) deletado(s) com sucesso.")
    deletar_backups.short_description = 'Deletar backups selecionados'

    def download_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" download>Download</a>', obj.file.url)
        return "-"
    download_link.short_description = "Download"

@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ('uploaded_at', 'file', 'description', 'instrucoes')
    search_fields = ('description',)
    actions = ['aplicar_update']
    readonly_fields = ('uploaded_at', 'file', 'description', 'instrucoes')
    fieldsets = (
        (None, {
            'fields': ('instrucoes', 'file', 'description', 'uploaded_at')
        }),
    )

    def instrucoes(self, obj=None):
        return mark_safe('<b>Atualização:</b> Faça upload de arquivos de atualização (ex: novos templates).<br>'
                         'Depois, selecione e use a ação para aplicar a atualização.<br>'
                         '<span style="color:#d9534f;">Atenção: arquivos podem ser sobrescritos!</span>')
    instrucoes.short_description = 'Instruções'

    def aplicar_update(self, request, queryset):
        for update in queryset:
            # Exemplo: copiar arquivo para o local correto (ajuste conforme sua estrutura)
            destino = os.path.join(settings.BASE_DIR, 'updates', os.path.basename(update.file.name))
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            with open(update.file.path, 'rb') as src, open(destino, 'wb') as dst:
                dst.write(src.read())
            self.message_user(request, f"Atualização aplicada: {update.file.name}")
    aplicar_update.short_description = 'Aplicar atualização selecionada'

def start_backup(request):
    backup_name = f"backup_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.dump"
    backup_path = os.path.join('backups', backup_name)
    task = backup_task.delay(backup_path)
    return JsonResponse({'task_id': task.id})

def backup_progress(request, task_id):
    result = AsyncResult(task_id)
    if result.state == 'PROGRESS':
        progress = result.info.get('progress', 0)
    elif result.state == 'SUCCESS':
        progress = 100
    else:
        progress = 0
    return JsonResponse({'state': result.state, 'progress': progress})
