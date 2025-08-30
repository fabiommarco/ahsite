import subprocess
from celery import shared_task
import os
import zipfile
from django.conf import settings
from gestao.models import Backup
from django.utils import timezone

@shared_task(bind=True)
def backup_task(self, backup_path):
    import time
    try:
        # Simula progresso (0 a 90%)
        for i in range(10):
            self.update_state(state='PROGRESS', meta={'progress': i*10})
            time.sleep(1)
        
        # Backup real
        result = subprocess.run(f"pg_dump -U postgres -F c -b -v -f '{backup_path}' ah", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            # Salvar no modelo Backup
            from django.core.files import File
            with open(backup_path, 'rb') as f:
                backup_obj = Backup.objects.create(
                    file=File(f, name=os.path.basename(backup_path)),
                    description=f"Backup gerado em {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}"
                )
            
            self.update_state(state='PROGRESS', meta={'progress': 100})
            return {'progress': 100, 'status': 'ok', 'backup_id': backup_obj.id}
        else:
            error_msg = f"Erro no pg_dump: {result.stderr}"
            self.update_state(state='PROGRESS', meta={'progress': 100, 'error': error_msg})
            return {'progress': 100, 'status': 'erro', 'message': error_msg}
    except Exception as e:
        error_msg = f"Erro na task: {str(e)}"
        self.update_state(state='PROGRESS', meta={'progress': 100, 'error': error_msg})
        return {'progress': 100, 'status': 'erro', 'message': error_msg}

@shared_task(bind=True)
def backup_completo_task(self):
    import time
    # Caminhos
    now = timezone.now().strftime('%Y-%m-%d_%H-%M-%S')
    base_dir = settings.BASE_DIR
    backups_dir = os.path.join(base_dir, 'backups')
    os.makedirs(backups_dir, exist_ok=True)
    dump_name = f"backup_{now}.dump"
    dump_path = os.path.join(backups_dir, dump_name)
    media_dir = os.path.join(base_dir, 'media')
    media_zip_name = f"media_{now}.zip"
    media_zip_path = os.path.join(backups_dir, media_zip_name)
    final_zip_name = f"backup_completo_{now}.zip"
    final_zip_path = os.path.join(backups_dir, final_zip_name)

    # 1. Backup do banco
    self.update_state(state='PROGRESS', meta={'progress': 10})
    result = subprocess.run(f"pg_dump -U postgres -F c -b -v -f '{dump_path}' ah", shell=True)
    if result.returncode != 0:
        return {'progress': 100, 'status': 'erro_dump'}

    # 2. Compactar media
    self.update_state(state='PROGRESS', meta={'progress': 40})
    with zipfile.ZipFile(media_zip_path, 'w', zipfile.ZIP_DEFLATED) as media_zip:
        for root, dirs, files in os.walk(media_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, media_dir)
                media_zip.write(abs_path, arcname=os.path.join('media', rel_path))

    # 3. Gerar zip final
    self.update_state(state='PROGRESS', meta={'progress': 70})
    with zipfile.ZipFile(final_zip_path, 'w', zipfile.ZIP_DEFLATED) as final_zip:
        final_zip.write(dump_path, arcname=dump_name)
        final_zip.write(media_zip_path, arcname=media_zip_name)

    # 4. Salvar no modelo Backup
    from django.core.files import File
    with open(final_zip_path, 'rb') as f:
        backup_obj = Backup.objects.create(
            file=File(f, name=final_zip_name),
            description=f"Backup completo (banco + media) gerado em {now}"
        )

    # Limpeza: (opcional) remover arquivos temporários
    os.remove(dump_path)
    os.remove(media_zip_path)

    self.update_state(state='PROGRESS', meta={'progress': 100})
    return {'progress': 100, 'status': 'ok', 'backup_id': backup_obj.id}

@shared_task(bind=True)
def restore_task(self, backup_file):
    import time
    import zipfile
    import tempfile
    
    # Simula progresso inicial
    self.update_state(state='PROGRESS', meta={'progress': 10})
    time.sleep(1)
    
    try:
        # Extrair backup se for zip
        if backup_file.endswith('.zip'):
            self.update_state(state='PROGRESS', meta={'progress': 30})
            with zipfile.ZipFile(backup_file, 'r') as zip_ref:
                zip_ref.extractall('temp_restore')
            
            # Procurar arquivo .dump
            dump_file = None
            for root, dirs, files in os.walk('temp_restore'):
                for file in files:
                    if file.endswith('.dump'):
                        dump_file = os.path.join(root, file)
                        break
                if dump_file:
                    break
        else:
            dump_file = backup_file
        
        if not dump_file:
            return {'progress': 100, 'status': 'erro', 'message': 'Arquivo de backup não encontrado'}
        
        # Restaurar banco
        self.update_state(state='PROGRESS', meta={'progress': 60})
        result = subprocess.run(f"pg_restore -U postgres -d ah -c -v '{dump_file}'", shell=True)
        
        # Limpeza
        if backup_file.endswith('.zip') and os.path.exists('temp_restore'):
            import shutil
            shutil.rmtree('temp_restore')
        
        if result.returncode == 0:
            return {'progress': 100, 'status': 'ok'}
        else:
            return {'progress': 100, 'status': 'erro', 'message': 'Falha na restauração'}
            
    except Exception as e:
        return {'progress': 100, 'status': 'erro', 'message': str(e)}

@shared_task(bind=True)
def update_task(self, update_file):
    import time
    import zipfile
    import tempfile
    
    # Simula progresso inicial
    self.update_state(state='PROGRESS', meta={'progress': 10})
    time.sleep(1)
    
    try:
        # Extrair update se for zip
        if update_file.endswith('.zip'):
            self.update_state(state='PROGRESS', meta={'progress': 30})
            with zipfile.ZipFile(update_file, 'r') as zip_ref:
                zip_ref.extractall('temp_update')
            
            # Procurar arquivos de update
            update_files = []
            for root, dirs, files in os.walk('temp_update'):
                for file in files:
                    if file.endswith('.sql'):
                        update_files.append(os.path.join(root, file))
        
        else:
            update_files = [update_file]
        
        if not update_files:
            return {'progress': 100, 'status': 'erro', 'message': 'Arquivos de update não encontrados'}
        
        # Aplicar updates
        self.update_state(state='PROGRESS', meta={'progress': 60})
        for sql_file in update_files:
            result = subprocess.run(f"psql -U postgres -d ah -f '{sql_file}'", shell=True)
            if result.returncode != 0:
                return {'progress': 100, 'status': 'erro', 'message': f'Falha ao aplicar {sql_file}'}
        
        # Limpeza
        if update_file.endswith('.zip') and os.path.exists('temp_update'):
            import shutil
            shutil.rmtree('temp_update')
        
        return {'progress': 100, 'status': 'ok'}
            
    except Exception as e:
        return {'progress': 100, 'status': 'erro', 'message': str(e)} 

@shared_task
def backup_site_task(backup_path):
    # Pastas e arquivos a serem incluídos no backup do site
    site_dirs = [
        'ahsite', 'app', 'gestao', 'systemtools', 'templates', 'static', 'requirements', 'manage.py'
    ]
    base_dir = settings.BASE_DIR
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in site_dirs:
            abs_path = os.path.join(base_dir, item)
            if os.path.isdir(abs_path):
                for root, dirs, files in os.walk(abs_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, base_dir)
                        zipf.write(file_path, arcname)
            elif os.path.isfile(abs_path):
                zipf.write(abs_path, item)
    return {'progress': 100, 'status': 'ok', 'backup_path': backup_path} 