#!/usr/bin/env python3
"""
Webhook para Deploy Automático Local
Este script pode ser executado como um serviço para monitorar mudanças no Git
"""

import os
import subprocess
import time
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('deploy.log'),
        logging.StreamHandler()
    ]
)

def run_command(command, cwd=None):
    """Executa um comando e retorna o resultado"""
    try:
        output = subprocess.check_output(command, shell=True, cwd=cwd, stderr=subprocess.STDOUT)
        return output
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao executar comando: {e}")
        logging.error(f"Stderr: {e.output}")
        return None

def check_git_changes():
    """Verifica se há mudanças no Git"""
    # Verificar se há commits novos
    result = run_command("git fetch origin")
    if result is None:
        return False
    
    # Verificar diferenças
    result = run_command("git log HEAD..origin/main --oneline")
    return result is not None and result.strip() != ""

def deploy():
    """Executa o deploy"""
    logging.info("🚀 Iniciando deploy automático...")
    
    # 1. Pull das mudanças
    logging.info("📥 Atualizando código...")
    result = run_command("git pull origin main")
    if result is None:
        logging.error("❌ Falha ao fazer pull")
        return False
    
    # 2. Ativar ambiente virtual e instalar dependências
    logging.info("🐍 Ativando ambiente virtual...")
    result = run_command("source .venv2/bin/activate && pip install -r requirements.txt")
    
    # 3. Executar migrações
    logging.info("🗄️ Executando migrações...")
    result = run_command("source .venv2/bin/activate && python3 manage.py migrate")
    
    # 4. Coletar arquivos estáticos
    logging.info("📁 Coletando arquivos estáticos...")
    result = run_command("source .venv2/bin/activate && python3 manage.py collectstatic --noinput")
    
    # 5. Reiniciar servidor (se necessário)
    logging.info("🔄 Reiniciando servidor...")
    # Aqui você pode adicionar comandos para reiniciar o servidor
    
    logging.info("✅ Deploy concluído com sucesso!")
    return True

def main():
    """Função principal do webhook"""
    logging.info("🔍 Iniciando monitoramento de mudanças...")
    
    while True:
        try:
            if check_git_changes():
                logging.info("📝 Mudanças detectadas no Git!")
                if deploy():
                    logging.info("🎉 Deploy realizado com sucesso!")
                else:
                    logging.error("❌ Falha no deploy!")
            else:
                logging.info("⏳ Nenhuma mudança detectada...")
            
            # Aguardar 5 minutos antes da próxima verificação
            time.sleep(300)
            
        except KeyboardInterrupt:
            logging.info("🛑 Monitoramento interrompido pelo usuário")
            break
        except Exception as e:
            logging.error(f"❌ Erro inesperado: {e}")
            time.sleep(60)  # Aguardar 1 minuto em caso de erro

if __name__ == "__main__":
    main()
