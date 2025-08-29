#!/bin/bash

# Script de Deploy Automático para o Site AH
# Este script será executado automaticamente quando houver mudanças no Git

echo "🚀 Iniciando deploy automático..."
echo "=================================="

# 1. Atualizar o código
echo "📥 Atualizando código..."
git pull origin main

# 2. Ativar ambiente virtual
echo "🐍 Ativando ambiente virtual..."
source .venv2/bin/activate

# 3. Instalar/atualizar dependências
echo "📦 Atualizando dependências..."
pip install -r requirements.txt

# 4. Executar migrações do banco
echo "🗄️ Executando migrações..."
python3 manage.py migrate

# 5. Coletar arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python3 manage.py collectstatic --noinput

# 6. Verificar se há novas notícias para processar
echo "📰 Verificando notícias..."
python3 manage.py shell -c "
from app.models import News
total = News.objects.count()
print(f'Total de notícias no banco: {total}')
"

# 7. Reiniciar serviços (se necessário)
echo "🔄 Reiniciando serviços..."
# Descomente as linhas abaixo se estiver usando systemd
# sudo systemctl restart ahsite
# sudo systemctl restart nginx

# 8. Verificar status
echo "✅ Verificando status..."
if [ $? -eq 0 ]; then
    echo "🎉 Deploy concluído com sucesso!"
    echo "🌐 Site disponível em: http://127.0.0.1:8000"
else
    echo "❌ Erro no deploy!"
    exit 1
fi

echo "=================================="
echo "Deploy finalizado em: $(date)"
