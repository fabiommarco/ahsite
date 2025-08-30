#!/bin/bash
# Script de Deploy Automático - Agropecuária AH
# Fabio Marco - 2025

set -e  # Parar em caso de erro

echo "🚀 Iniciando deploy automático..."
echo "📅 Data/Hora: $(date)"
echo "=================================="

# Configurações
PROJECT_DIR="/var/www/ahsite_news/ahsite/ahsite"
BACKUP_DIR="/var/www/ahsite_news/ahsite/backups"
LOG_FILE="/var/www/ahsite_news/ahsite/deploy.log"

# Criar diretório de backup se não existir
mkdir -p "$BACKUP_DIR"

# Função para log
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Backup do banco antes do deploy
log "💾 Fazendo backup do banco..."
cd "$PROJECT_DIR"
python manage.py dumpdata > "$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).json"

# Git pull
log "📥 Fazendo git pull..."
cd "$PROJECT_DIR"
git pull origin master || {
    log "❌ Erro no git pull"
    exit 1
}

# Instalar dependências se necessário
log "📦 Verificando dependências..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Coletar arquivos estáticos
log "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Executar migrações
log "🗄️ Executando migrações..."
python manage.py migrate --noinput

# Verificar sintaxe Python
log "🔍 Verificando sintaxe Python..."
find . -name "*.py" -exec python -m py_compile {} \;

# Reiniciar serviços
log "🔄 Reiniciando serviços..."
systemctl restart nginx || true
systemctl restart gunicorn || true

# Verificar se o site está funcionando
log "✅ Verificando se o site está online..."
sleep 5
if curl -f http://localhost:8000/ > /dev/null 2>&1; then
    log "✅ Site está funcionando corretamente!"
else
    log "⚠️ Site pode não estar respondendo"
fi

log "🎉 Deploy concluído com sucesso!"
echo "=================================="
