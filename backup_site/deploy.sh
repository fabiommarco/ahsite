#!/bin/bash

echo "🚀 Deploy Automático - Site AH"
echo "=================================="

# Configurações
PROJECT_DIR="/var/www/ahsite_news/ahsite/ahsite"
VENV_PATH="/var/www/ahsite_news/ahsite/backup_site/venv"
GIT_REPO="/var/www/ahsite_news/ahsite/backup_site"

# Função de log
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 1. Atualizar código do Git
log "📥 Atualizando código do Git..."
cd $GIT_REPO
git fetch origin
git reset --hard origin/master

# 2. Copiar arquivos para o diretório do projeto
log "📁 Copiando arquivos..."
cp -r app/* $PROJECT_DIR/app/
cp -r static/* $PROJECT_DIR/static/
cp -r templates/* $PROJECT_DIR/templates/
cp manage.py $PROJECT_DIR/
cp requirements.txt $PROJECT_DIR/

# 3. Ativar ambiente virtual
log "🐍 Ativando ambiente virtual..."
source $VENV_PATH/bin/activate

# 4. Instalar dependências
log "📦 Instalando dependências..."
cd $PROJECT_DIR
pip install -r requirements.txt

# 5. Aplicar migrações
log "🗄️ Aplicando migrações..."
python3 manage.py migrate

# 6. Coletar arquivos estáticos
log "📁 Coletando arquivos estáticos..."
python3 manage.py collectstatic --noinput

# 7. Verificar se o Django está funcionando
log "🔍 Verificando Django..."
python3 manage.py check

# 8. Reiniciar serviços (se necessário)
log "🔄 Reiniciando serviços..."
# Aqui você pode adicionar comandos específicos da Locaweb
# Por exemplo, reiniciar o servidor web

log "✅ Deploy concluído com sucesso!"
log "🌐 Site disponível em: http://seudominio.com"
echo "=================================="
log "Deploy finalizado em: $(date)"
