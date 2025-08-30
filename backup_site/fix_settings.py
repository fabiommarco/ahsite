#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir o arquivo settings.py removendo chaves extras
"""

import os
import re

def fix_settings_file(file_path):
    """Corrige o arquivo settings.py removendo chaves extras"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove chaves extras após DATABASES
    # Padrão: DATABASES = { ... }, }, }
    content = re.sub(r'DATABASES\s*=\s*\{[^}]*\},?\s*\},?\s*\}', 
                    lambda m: m.group(0).replace(',},', '}').replace('},}', '}'), 
                    content, flags=re.DOTALL)
    
    # Remove chaves extras soltas
    content = re.sub(r'\},?\s*\},?\s*\}', '}', content)
    
    # Corrige BASE_DIR / 'db.sqlite3' para os.path.join(BASE_DIR, 'db.sqlite3')
    content = re.sub(r"BASE_DIR\s*/\s*'db\.sqlite3'", "os.path.join(BASE_DIR, 'db.sqlite3')", content)
    
    # Salva o arquivo corrigido
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Arquivo {file_path} corrigido com sucesso!")

if __name__ == "__main__":
    settings_file = "ahsite/settings.py"
    if os.path.exists(settings_file):
        fix_settings_file(settings_file)
    else:
        print(f"Arquivo {settings_file} não encontrado!")
