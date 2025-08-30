from django.http import JsonResponse
from gestao.tasks import backup_task, restore_task, update_task
from celery.result import AsyncResult
import os
import datetime
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

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

def backup_page(request):
    return render(request, 'gestao/backup_page.html')

# Endpoint para iniciar backup via AJAX
@csrf_exempt
def start_backup_ajax(request):
    print("=== INICIANDO start_backup_ajax ===")
    try:
        tipo_backup = request.POST.get('tipo_backup', 'banco')
        print(f"Tipo de backup solicitado: {tipo_backup}")
        backup_name = f"backup_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        if tipo_backup == 'banco':
            backup_path = os.path.join(backup_dir, f"{backup_name}.dump")
            task = backup_task.delay(backup_path)
        elif tipo_backup == 'site':
            backup_path = os.path.join(backup_dir, f"{backup_name}_site.zip")
            from gestao.tasks import backup_site_task
            task = backup_site_task.delay(backup_path)
        elif tipo_backup == 'completo':
            from gestao.tasks import backup_completo_task
            task = backup_completo_task.delay()
        else:
            return JsonResponse({'error': 'Tipo de backup inválido.'}, status=400)
        return JsonResponse({'task_id': task.id, 'status': 'success'})
    except Exception as e:
        print(f"=== ERRO em start_backup_ajax: {str(e)} ===")
        import traceback
        print("Traceback completo:")
        print(traceback.format_exc())
        return JsonResponse({'error': str(e)}, status=500)

# Página de restauração
@csrf_exempt
def restore_page(request):
    return render(request, 'gestao/restore_page.html')

# Endpoint AJAX para restaurar backup
@csrf_exempt
def start_restore_ajax(request):
    import json
    data = json.loads(request.body)
    backup_file = data.get('backup_file')
    task = restore_task.delay(backup_file)
    return JsonResponse({'task_id': task.id})

# Página de update
@csrf_exempt
def update_page(request):
    return render(request, 'gestao/update_page.html')

# Endpoint AJAX para aplicar update
@csrf_exempt
def start_update_ajax(request):
    import json
    data = json.loads(request.body)
    update_file = data.get('update_file')
    task = update_task.delay(update_file)
    return JsonResponse({'task_id': task.id})