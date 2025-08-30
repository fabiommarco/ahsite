#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sistema de Commit Automático - Agropecuária AH
Fabio Marco - 2025
fabio.marco@ah.agr.br

Este script:
1. Detecta mudanças automaticamente
2. Faz commit com mensagem inteligente
3. Faz push para o repositório
4. Executa deploy automático
"""

import os
import sys
import subprocess
import datetime
import json
from pathlib import Path

def executar_comando(comando, cwd=None):
    """Executa um comando e retorna o resultado"""
    try:
        resultado = subprocess.check_output(
            comando, 
            shell=True, 
            stderr=subprocess.STDOUT, 
            cwd=cwd,
            universal_newlines=True
        )
        return True, resultado
    except subprocess.CalledProcessError as e:
        return False, e.output

def detectar_mudancas():
    """Detecta quais arquivos foram modificados"""
    print("🔍 Detectando mudanças...")

    # Verificar status do git
    sucesso, resultado = executar_comando("git status --porcelain")
    if not sucesso:
        return []

    arquivos_modificados = []
    for linha in resultado.strip().split('\n'):
        if linha:
            status = linha[:2]
            arquivo = linha[3:]
            arquivos_modificados.append({
                'status': status,
                'arquivo': arquivo
            })

    return arquivos_modificados

def gerar_mensagem_commit(arquivos):
    """Gera uma mensagem de commit inteligente baseada nas mudanças"""
    if not arquivos:
        return "chore: Atualização automática"

    # Contar tipos de mudanças
    tipos = {
        'M': 'modificado',
        'A': 'adicionado', 
        'D': 'removido',
        'R': 'renomeado'
    }

    contadores = {}
    for arquivo in arquivos:
        status = arquivo['status'][0]  # Primeiro caractere
        if status in tipos:
            contadores[tipos[status]] = contadores.get(tipos[status], 0) + 1

    # Gerar mensagem
    partes = []
    for tipo, count in contadores.items():
        if count == 1:
            partes.append(f"1 arquivo {tipo}")
        else:
            partes.append(f"{count} arquivos {tipos[tipo]}")

    mensagem = f"feat: {' e '.join(partes)}"

    # Adicionar detalhes importantes
    arquivos_importantes = []
    for arquivo in arquivos:
        nome = arquivo['arquivo']
        if any(keyword in nome.lower() for keyword in ['views.py', 'urls.py', 'models.py', 'admin.py', 'settings.py']):
            arquivos_importantes.append(nome)

    if arquivos_importantes:
        mensagem += f"\n\nArquivos principais: {', '.join(arquivos_importantes[:3])}"

    return mensagem

def fazer_commit_automatico():
    """Executa o commit automático completo"""
    print("🚀 Iniciando commit automático...")
    print("=" * 50)

    # 1. Detectar mudanças
    arquivos = detectar_mudancas()

    if not arquivos:
        print("✅ Nenhuma mudança detectada!")
        return True, "Nenhuma mudança para commitar"

    print(f"📝 {len(arquivos)} arquivo(s) modificado(s):")
    for arquivo in arquivos[:5]:  # Mostrar apenas os primeiros 5
        print(f"   {arquivo['status']} {arquivo['arquivo']}")
    if len(arquivos) > 5:
        print(f"   ... e mais {len(arquivos) - 5} arquivo(s)")

    # 2. Adicionar todos os arquivos
    print("\n📦 Adicionando arquivos...")
    sucesso, resultado = executar_comando("git add .")
    if not sucesso:
        return False, f"Erro ao adicionar arquivos: {resultado}"

    # 3. Gerar mensagem de commit
    mensagem = gerar_mensagem_commit(arquivos)
    print(f"\n💬 Mensagem de commit: {mensagem}")

    # 4. Fazer commit
    print("\n💾 Fazendo commit...")
    sucesso, resultado = executar_comando(f'git commit -m "{mensagem}"')
    if not sucesso:
        return False, f"Erro no commit: {resultado}"

    print("✅ Commit realizado com sucesso!")

    # 5. Fazer push
    print("\n📤 Fazendo push...")
    # Configurar credenciais temporariamente
    sucesso, resultado = executar_comando("git config credential.helper store")
    sucesso, resultado = executar_comando("git push origin master")
    if not sucesso:
        return False, f"Erro no push: {resultado}"

    print("✅ Push realizado com sucesso!")

    # 6. Executar deploy (opcional)
    print("\n🚀 Executando deploy automático...")
    sucesso, resultado = executar_comando("curl -X POST http://localhost:8000/deploy/")
    if sucesso:
        print("✅ Deploy executado!")
    else:
        print("⚠️ Deploy não executado (servidor pode estar offline)")

    return True, "Commit e push realizados com sucesso!"

def main():
    """Função principal"""
    print("🤖 Sistema de Commit Automático - Agropecuária AH")
    print("=" * 60)

    try:
        sucesso, mensagem = fazer_commit_automatico()

        print("\n" + "=" * 60)
        if sucesso:
            print("✅ SUCESSO!")
            print(f"📋 {mensagem}")
        else:
            print("❌ ERRO!")
            print(f"📋 {mensagem}")

        return sucesso

    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
