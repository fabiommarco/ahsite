#!/bin/bash
echo "🚀 Deploy para Locaweb - Site AH"
echo "=================================="

# Configurações
REPO_URL="https://github.com/SEU-USUARIO/ahsite.git"
LOCAL_PATH="/mnt/c/Users/fabiommarco/documents/backup_ah/backup_site"
BRANCH="master"

echo "📥 Atualizando código do GitHub..."
cd "$LOCAL_PATH"

# Fazer pull das últimas mudanças
git pull origin $BRANCH

if [ $? -eq 0 ]; then
    echo "✅ Código atualizado com sucesso!"
    
    echo "🐍 Ativando ambiente virtual..."
    source .venv2/bin/activate
    
    echo "📦 Verificando dependências..."
    pip install -r requirements.txt
    
    echo "🗄️ Executando migrações..."
    python3 manage.py migrate
    
    echo "📁 Coletando arquivos estáticos..."
    python3 manage.py collectstatic --noinput
    
    echo "📰 Verificando notícias..."
    python3 manage.py shell -c "
from app.models import News
total = News.objects.count()
print(f'Total de notícias: {total}')
"
    
    echo "🔄 Reiniciando serviços..."
    # Aqui você pode adicionar comandos específicos da Locaweb
    # Por exemplo, reiniciar o servidor web
    
    echo "✅ Deploy concluído com sucesso!"
    echo "🌐 Site disponível em: https://seudominio.com"
    
else
    echo "❌ Erro ao atualizar código!"
    exit 1
fi

echo "=================================="
echo "Deploy finalizado em: $(date)"
