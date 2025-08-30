#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir o arquivo settings.py no servidor da Locaweb
Remove chaves extras e corrige sintaxe
"""

import os
import re

def fix_locaweb_settings():
    """Corrige o arquivo settings.py no servidor da Locaweb"""
    
    settings_file = "ahsite/settings.py"
    
    if not os.path.exists(settings_file):
        print(f"Arquivo {settings_file} não encontrado!")
        return False
    
    # Faz backup
    backup_file = f"{settings_file}.backup"
    os.system(f"cp {settings_file} {backup_file}")
    print(f"Backup criado: {backup_file}")
    
    with open(settings_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Remove chaves extras nas linhas 80-85
    fixed_lines = []
    for i, line in enumerate(lines, 1):
        if 80 <= i <= 85:
            # Remove chaves extras
            line = re.sub(r'},?\s*},?\s*}', '}', line)
            line = re.sub(r'},?\s*},?\s*$', '}', line)
        fixed_lines.append(line)
    
    # Corrige BASE_DIR / 'db.sqlite3'
    content = ''.join(fixed_lines)
    content = re.sub(r"BASE_DIR\s*/\s*'db\.sqlite3'", "os.path.join(BASE_DIR, 'db.sqlite3')", content)
    
    # Salva o arquivo corrigido
    with open(settings_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Arquivo {settings_file} corrigido com sucesso!")
    return True

if __name__ == "__main__":
    fix_locaweb_settings()
