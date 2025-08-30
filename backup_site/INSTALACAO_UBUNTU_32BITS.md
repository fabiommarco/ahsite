# Instalação no Ubuntu 18.04 32 bits

## ⚠️ IMPORTANTE: Sistema 32 bits

Este projeto foi configurado especificamente para Ubuntu 18.04 32 bits. As versões das dependências foram ajustadas para máxima compatibilidade.

## 📋 Pré-requisitos do Sistema

```bash
# Atualizar o sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python 3.6 (padrão no Ubuntu 18.04)
sudo apt install -y python3 python3-pip python3-dev

# Instalar dependências do sistema para 32 bits
sudo apt install -y build-essential libssl-dev libffi-dev
sudo apt install -y libpq-dev postgresql postgresql-contrib
sudo apt install -y libmysqlclient-dev default-libmysqlclient-dev
sudo apt install -y redis-server

# Instalar dependências específicas para 32 bits
sudo apt install -y libjpeg-dev zlib1g-dev libfreetype6-dev
sudo apt install -y liblcms2-dev libopenjp2-7-dev libtiff5-dev
sudo apt install -y libwebp-dev libharfbuzz-dev libfribidi-dev
sudo apt install -y libxcb1-dev
```

## 🐍 Configuração do Python

```bash
# Criar ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate

# Atualizar pip
pip install --upgrade pip setuptools wheel
```

## 📦 Instalação das Dependências

### Para Desenvolvimento:
```bash
pip install -r requirements/dev.txt
```

### Para Produção:
```bash
pip install -r requirements/prod.txt
```

### Para Todas as Dependências:
```bash
pip install -r requirements.txt
```

## 🔧 Configurações Específicas para 32 bits

### PostgreSQL:
```bash
# Configurar PostgreSQL
sudo -u postgres createuser --interactive
sudo -u postgres createdb ah
```

### Redis:
```bash
# Iniciar Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

## 🚀 Executar o Projeto

```bash
# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar servidor de desenvolvimento
python manage.py runserver 0.0.0.0:8000
```

## ⚠️ Limitações Conhecidas

1. **Memória**: Sistemas 32 bits têm limitação de 4GB de RAM
2. **Processamento**: Algumas operações podem ser mais lentas
3. **Compatibilidade**: Algumas bibliotecas mais recentes não funcionam

## 🔍 Solução de Problemas

### Erro de compilação:
```bash
# Se houver problemas com Pillow
sudo apt install -y python3-dev libjpeg-dev zlib1g-dev
pip install --no-cache-dir Pillow==8.4.0
```

### Erro de psycopg2:
```bash
# Instalar dependências do PostgreSQL
sudo apt install -y libpq-dev
pip install --no-cache-dir psycopg2-binary==2.9.5
```

### Erro de mysqlclient:
```bash
# Instalar dependências do MySQL
sudo apt install -y libmysqlclient-dev
pip install --no-cache-dir mysqlclient==2.0.3
```

## 📝 Notas Importantes

- Use sempre as versões especificadas nos requirements
- Evite atualizar para versões mais recentes sem testar
- Monitore o uso de memória durante a execução
- Considere usar um servidor de produção mais robusto para 32 bits 