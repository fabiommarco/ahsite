# Comandos para corrigir o settings.py no servidor da Locaweb

## 1. Acesse o servidor via SSH
```bash
ssh usuario@seu-servidor.locaweb.com.br
```

## 2. Navegue até o diretório do projeto
```bash
cd /var/www/ahsite_news/ahsite/ahsite
```

## 3. Ative o ambiente virtual
```bash
source venv/bin/activate
```

## 4. Faça backup do arquivo atual
```bash
cp ahsite/settings.py ahsite/settings.py.backup
```

## 5. Corrija o arquivo usando sed (método rápido)
```bash
# Remove chaves extras nas linhas 80-85
sed -i '80,85s/},},},/},/' ahsite/settings.py
sed -i '80,85s/},},/},/' ahsite/settings.py

# Corrige BASE_DIR / 'db.sqlite3'
sed -i "s/BASE_DIR \/ 'db.sqlite3'/os.path.join(BASE_DIR, 'db.sqlite3')/g" ahsite/settings.py
```

## 6. Ou use o script Python (método alternativo)
```bash
# Copie o script para o servidor
python fix_locaweb_settings.py
```

## 7. Verifique a sintaxe
```bash
python -m py_compile ahsite/settings.py
```

## 8. Teste o Django
```bash
python manage.py check
```

## 9. Se tudo estiver OK, reinicie o servidor web
```bash
# Para Apache
sudo systemctl restart apache2

# Para Nginx
sudo systemctl restart nginx

# Ou reinicie o serviço específico da Locaweb
```

## 10. Verifique os logs se houver problemas
```bash
tail -f /var/log/apache2/error.log
# ou
tail -f /var/log/nginx/error.log
```

## Comandos de emergência (se algo der errado)

### Restaurar backup
```bash
cp ahsite/settings.py.backup ahsite/settings.py
```

### Verificar permissões
```bash
chmod 644 ahsite/settings.py
chown www-data:www-data ahsite/settings.py
```

### Verificar se o Django está funcionando
```bash
python manage.py runserver 0.0.0.0:8000
```
