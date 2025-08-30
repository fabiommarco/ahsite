#!/bin/bash
# Script para corrigir problemas no servidor da Locaweb
# Execute este script no servidor da Locaweb

echo "=== CORRIGINDO PROBLEMAS NO SERVIDOR LOCAWEB ==="

# 1. Corrigir encoding no admin.py
echo "1. Corrigindo encoding no admin.py..."
if ! grep -q "coding: utf-8" app/admin.py; then
    sed -i '1i# -*- coding: utf-8 -*-' app/admin.py
    echo "   ✓ Encoding adicionado ao admin.py"
else
    echo "   ✓ Encoding já existe no admin.py"
fi

# 2. Corrigir chaves extras no settings.py
echo "2. Corrigindo chaves extras no settings.py..."
sed -i '83,84d' ahsite/settings.py
echo "   ✓ Chaves extras removidas do settings.py"

# 3. Corrigir BASE_DIR no settings.py
echo "3. Corrigindo BASE_DIR no settings.py..."
sed -i "s/BASE_DIR \/ 'db.sqlite3'/os.path.join(BASE_DIR, 'db.sqlite3')/g" ahsite/settings.py
echo "   ✓ BASE_DIR corrigido no settings.py"

# 4. Corrigir views.py - remover referência ao Banner
echo "4. Corrigindo views.py..."
sed -i '/banners = Banner.objects.filter(ativo=True).order_by/d' app/views.py
sed -i 's/banners = \[\]/banners = []/' app/views.py
echo "   ✓ Views.py corrigido"

# 5. Testar sintaxe
echo "5. Testando sintaxe..."
python -m py_compile ahsite/settings.py
python -m py_compile app/admin.py
python -m py_compile app/views.py
echo "   ✓ Sintaxe OK"

# 6. Testar Django
echo "6. Testando Django..."
python manage.py check
echo "   ✓ Django OK"

echo "=== CORREÇÕES CONCLUÍDAS ==="
echo "Agora você pode iniciar o servidor:"
echo "python manage.py runserver 0.0.0.0:8000 --noreload &"
