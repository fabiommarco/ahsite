#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Backup para WSL - AH Site
Autor: Fábio Marco
Data: 2025-07-08
"""

import os
import sys
import subprocess
import datetime
import zipfile
import shutil
from pathlib import Path

# Configurações
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
DB_NAME = 'ah'
DB_USER = 'postgres'
DB_PASSWORD = 'Deus@2025'

def criar_diretorio_backup():
    """Cria o diretório de backup se não existir"""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    print(f"✓ Diretório de backup: {BACKUP_DIR}")

def backup_banco_dados():
    """Faz backup do banco de dados PostgreSQL"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    dump_file = os.path.join(BACKUP_DIR, f'backup_banco_{timestamp}.dump')
    
    print(f"🔄 Iniciando backup do banco de dados...")
    
    # Comando pg_dump para WSL
    cmd = [
        'wsl', '--exec', 'bash', '-c',
        f'PGPASSWORD={DB_PASSWORD} pg_dump -U {DB_USER} -h localhost -F c -b -v -f "{dump_file}" {DB_NAME}'
    ]
    
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        print(f"✓ Backup do banco concluído: {dump_file}")
        return dump_file
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no backup do banco: {e}")
        print(f"Stderr: {e.output}")
        return None

def backup_media():
    """Faz backup da pasta media"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    media_zip = os.path.join(BACKUP_DIR, f'backup_media_{timestamp}.zip')
    
    print(f"🔄 Iniciando backup da pasta media...")
    
    try:
        with zipfile.ZipFile(media_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if os.path.exists(MEDIA_DIR):
                for root, dirs, files in os.walk(MEDIA_DIR):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, MEDIA_DIR)
                        zipf.write(file_path, arcname)
                        print(f"  📁 Adicionado: {arcname}")
            else:
                print("⚠️  Pasta media não encontrada")
        
        print(f"✓ Backup da media concluído: {media_zip}")
        return media_zip
    except Exception as e:
        print(f"❌ Erro no backup da media: {e}")
        return None

def backup_site():
    """Faz backup dos arquivos do site (código fonte)"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    site_zip = os.path.join(BACKUP_DIR, f'backup_site_{timestamp}.zip')
    
    print(f"🔄 Iniciando backup dos arquivos do site...")
    
    # Pastas e arquivos a serem incluídos
    site_items = [
        'ahsite', 'app', 'gestao', 'systemtools', 'templates', 
        'static', 'requirements', 'manage.py', 'requirements.txt'
    ]
    
    try:
        with zipfile.ZipFile(site_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for item in site_items:
                item_path = os.path.join(BASE_DIR, item)
                if os.path.exists(item_path):
                    if os.path.isdir(item_path):
                        for root, dirs, files in os.walk(item_path):
                            # Ignorar diretórios desnecessários
                            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'venv', '.venv', 'node_modules']]
                            for file in files:
                                if not file.endswith(('.pyc', '.log', '.tmp')):
                                    file_path = os.path.join(root, file)
                                    arcname = os.path.relpath(file_path, BASE_DIR)
                                    zipf.write(file_path, arcname)
                    else:
                        zipf.write(item_path, item)
        
        print(f"✓ Backup do site concluído: {site_zip}")
        return site_zip
    except Exception as e:
        print(f"❌ Erro no backup do site: {e}")
        return None

def backup_completo():
    """Faz backup completo (banco + media + site)"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    completo_zip = os.path.join(BACKUP_DIR, f'backup_completo_{timestamp}.zip')
    
    print(f"🔄 Iniciando backup completo...")
    
    # Fazer backups individuais
    dump_file = backup_banco_dados()
    media_zip = backup_media()
    site_zip = backup_site()
    
    if not dump_file:
        print("❌ Falha no backup do banco. Abortando backup completo.")
        return None
    
    # Criar zip completo
    try:
        with zipfile.ZipFile(completo_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Adicionar backup do banco
            zipf.write(dump_file, os.path.basename(dump_file))
            
            # Adicionar backup da media se existir
            if media_zip and os.path.exists(media_zip):
                zipf.write(media_zip, os.path.basename(media_zip))
            
            # Adicionar backup do site se existir
            if site_zip and os.path.exists(site_zip):
                zipf.write(site_zip, os.path.basename(site_zip))
        
        print(f"✓ Backup completo concluído: {completo_zip}")
        
        # Limpar arquivos temporários
        if os.path.exists(dump_file):
            os.remove(dump_file)
        if media_zip and os.path.exists(media_zip):
            os.remove(media_zip)
        if site_zip and os.path.exists(site_zip):
            os.remove(site_zip)
        
        return completo_zip
    except Exception as e:
        print(f"❌ Erro no backup completo: {e}")
        return None

def listar_backups():
    """Lista todos os backups existentes"""
    print(f"\n📋 Backups existentes em {BACKUP_DIR}:")
    print("-" * 60)
    
    if not os.path.exists(BACKUP_DIR):
        print("Nenhum backup encontrado.")
        return
    
    backups = []
    for file in os.listdir(BACKUP_DIR):
        if file.endswith(('.dump', '.zip')):
            file_path = os.path.join(BACKUP_DIR, file)
            size = os.path.getsize(file_path)
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            backups.append((file, size, mtime))
    
    if not backups:
        print("Nenhum backup encontrado.")
        return
    
    # Ordenar por data (mais recente primeiro)
    backups.sort(key=lambda x: x[2], reverse=True)
    
    for file, size, mtime in backups:
        size_mb = size / (1024 * 1024)
        print(f"📁 {file}")
        print(f"   📅 {mtime.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"   📊 {size_mb:.2f} MB")
        print()

def main():
    """Função principal"""
    print("🚀 Script de Backup AH Site - WSL")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Uso: python backup_wsl.py [opção]")
        print("\nOpções:")
        print("  banco     - Backup apenas do banco de dados")
        print("  media     - Backup apenas da pasta media")
        print("  site      - Backup apenas dos arquivos do site")
        print("  completo  - Backup completo (banco + media + site)")
        print("  listar    - Listar backups existentes")
        return
    
    opcao = sys.argv[1].lower()
    
    criar_diretorio_backup()
    
    if opcao == 'banco':
        backup_banco_dados()
    elif opcao == 'media':
        backup_media()
    elif opcao == 'site':
        backup_site()
    elif opcao == 'completo':
        backup_completo()
    elif opcao == 'listar':
        listar_backups()
    else:
        print(f"❌ Opção inválida: {opcao}")
        return
    
    print("\n✅ Processo concluído!")

if __name__ == "__main__":
    main() 