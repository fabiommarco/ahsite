#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar e corrigir o arquivo settings.py
"""

import os

def verificar_e_corrigir_settings():
    """Verifica e corrige o arquivo settings.py"""
    
    settings_file = "ahsite/settings.py"
    
    if not os.path.exists(settings_file):
        print(f"Arquivo {settings_file} não encontrado!")
        return False
    
    # Lê o arquivo
    with open(settings_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print("=== VERIFICANDO LINHAS 75-90 ===")
    for i, line in enumerate(lines[74:90], 75):
        print(f"Linha {i}: {repr(line.rstrip())}")
    
    print("\n=== CORRIGINDO O ARQUIVO ===")
    
    # Corrige o arquivo manualmente
    corrected_lines = []
    in_databases = False
    brace_count = 0
    
    for i, line in enumerate(lines):
        original_line = line
        
        # Detecta início do DATABASES
        if 'DATABASES = {' in line:
            in_databases = True
            brace_count = 1
            corrected_lines.append(line)
            continue
        
        # Se estamos dentro do DATABASES
        if in_databases:
            # Conta chaves
            brace_count += line.count('{') - line.count('}')
            
            # Se fechou o DATABASES
            if brace_count == 0:
                in_databases = False
                corrected_lines.append(line)
                continue
            
            # Remove chaves extras
            if '},' in line and brace_count == 1:
                line = line.replace('},},', '},')
                line = line.replace('},},},', '},')
                line = line.replace('},},},},', '},')
            
            corrected_lines.append(line)
        else:
            corrected_lines.append(line)
    
    # Corrige BASE_DIR
    content = ''.join(corrected_lines)
    content = content.replace("BASE_DIR / 'db.sqlite3'", "os.path.join(BASE_DIR, 'db.sqlite3')")
    
    # Salva o arquivo corrigido
    with open(settings_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Arquivo corrigido!")
    return True

if __name__ == "__main__":
    verificar_e_corrigir_settings()
