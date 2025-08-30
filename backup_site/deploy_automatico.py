#!/usr/bin/env python3
"""
Script de Deploy Automático Local
Monitora mudanças nos arquivos e executa deploy automaticamente
"""

import os
import time
import subprocess
import logging
from datetime import datetime
from pathlib import Path
import hashlib

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('deploy_automatico.log'),
        logging.StreamHandler()
    ]
)

class DeployAutomatico:
    def __init__(self):
        self.projeto_path = Path("/mnt/c/Users/fabiommarco/documents/backup_ah/backup_site")
        self.arquivos_monitorados = [
            "app/admin.py",
            "app/views.py", 
            "app/models.py",
            "static/js/contact_me.js",
            "templates/",
            "static/css/",
            "static/js/"
        ]
        self.ultimo_hash = {}
        self.ultimo_deploy = None
        
    def calcular_hash_arquivo(self, arquivo_path):
        """Calcula o hash MD5 de um arquivo"""
        try:
            with open(arquivo_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            logging.error(f"Erro ao calcular hash de {arquivo_path}: {e}")
            return None
    
    def verificar_mudancas(self):
        """Verifica se houve mudanças nos arquivos monitorados"""
        mudancas_detectadas = []
        
        for arquivo in self.arquivos_monitorados:
            caminho_completo = self.projeto_path / arquivo
            
            if caminho_completo.is_file():
                # Arquivo individual
                hash_atual = self.calcular_hash_arquivo(caminho_completo)
                if hash_atual and hash_atual != self.ultimo_hash.get(str(caminho_completo)):
                    mudancas_detectadas.append(str(caminho_completo))
                    self.ultimo_hash[str(caminho_completo)] = hash_atual
                    
            elif caminho_completo.is_dir():
                # Diretório - verificar todos os arquivos
                for arquivo_dentro in caminho_completo.rglob('*'):
                    if arquivo_dentro.is_file():
                        hash_atual = self.calcular_hash_arquivo(arquivo_dentro)
                        if hash_atual and hash_atual != self.ultimo_hash.get(str(arquivo_dentro)):
                            mudancas_detectadas.append(str(arquivo_dentro))
                            self.ultimo_hash[str(arquivo_dentro)] = hash_atual
        
        return mudancas_detectadas
    
    def executar_deploy(self):
        """Executa o deploy"""
        try:
            logging.info("🚀 Iniciando deploy automático...")
            
            # Executar o script de deploy
            resultado = subprocess.run(
                ["./deploy.sh"],
                cwd=self.projeto_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=300  # 5 minutos de timeout
            )
            
            if resultado.returncode == 0:
                logging.info("✅ Deploy executado com sucesso!")
                self.ultimo_deploy = datetime.now()
                return True
            else:
                logging.error(f"❌ Erro no deploy: {resultado.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logging.error("❌ Timeout no deploy (mais de 5 minutos)")
            return False
        except Exception as e:
            logging.error(f"❌ Erro ao executar deploy: {e}")
            return False
    
    def executar_comando(self, comando, cwd=None):
        """Executa um comando e retorna o resultado"""
        try:
            resultado = subprocess.run(
                comando,
                shell=True,
                cwd=cwd or self.projeto_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60
            )
            return resultado.returncode == 0, resultado.stdout, resultado.stderr
        except Exception as e:
            return False, "", str(e)
    
    def iniciar_monitoramento(self):
        """Inicia o monitoramento contínuo"""
        logging.info("🔍 Iniciando monitoramento de arquivos...")
        logging.info(f"📁 Monitorando: {', '.join(self.arquivos_monitorados)}")
        logging.info("⏳ Verificando mudanças a cada 30 segundos...")
        logging.info("🛑 Pressione Ctrl+C para parar")
        
        # Inicializar hashes
        for arquivo in self.arquivos_monitorados:
            caminho_completo = self.projeto_path / arquivo
            if caminho_completo.is_file():
                self.ultimo_hash[str(caminho_completo)] = self.calcular_hash_arquivo(caminho_completo)
            elif caminho_completo.is_dir():
                for arquivo_dentro in caminho_completo.rglob('*'):
                    if arquivo_dentro.is_file():
                        self.ultimo_hash[str(arquivo_dentro)] = self.calcular_hash_arquivo(arquivo_dentro)
        
        try:
            while True:
                mudancas = self.verificar_mudancas()
                
                if mudancas:
                    logging.info(f"📝 Mudanças detectadas em {len(mudancas)} arquivo(s):")
                    for mudanca in mudancas[:5]:  # Mostrar apenas os primeiros 5
                        logging.info(f"   - {mudanca}")
                    if len(mudancas) > 5:
                        logging.info(f"   ... e mais {len(mudancas) - 5} arquivo(s)")
                    
                    # Aguardar um pouco para garantir que o arquivo foi salvo completamente
                    time.sleep(2)
                    
                    # Executar deploy
                    if self.executar_deploy():
                        logging.info("🎉 Deploy automático concluído!")
                    else:
                        logging.error("❌ Falha no deploy automático!")
                else:
                    logging.info("⏳ Nenhuma mudança detectada...")
                
                # Aguardar 30 segundos antes da próxima verificação
                time.sleep(30)
                
        except KeyboardInterrupt:
            logging.info("🛑 Monitoramento interrompido pelo usuário")
        except Exception as e:
            logging.error(f"❌ Erro no monitoramento: {e}")

def main():
    deploy = DeployAutomatico()
    deploy.iniciar_monitoramento()

if __name__ == "__main__":
    main()
