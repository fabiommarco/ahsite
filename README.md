# Agropecuária AH

## Dependências

Este projeto assume que as seguintes dependências estejam instaladas:

- `python2.7`
- `virtualenv` ou `virtualenvwrapper`
- `MySQL` ou `PostgreSQL`

## Configurações

Crie um ambiente virtual usando `virtualenv,` or `virtualenvwrapper.`

```bash
$ virtualenv -p /usr/bin/python2.7 env
$ env/bin/activate
```

Instale as dependências:

```bash
$ pip install -r requirements/dev.txt
```

## Desenvolvimento Local

Para executar o projeto, é necessário que um banco de dados já tenha sido 
configurado. As credenciais padrão podem ser sobrescritas através de
variávies de ambiente.

```bash
$ DB_NAME=ahsite DB_USER=root DB_PASSWORD=senha
$ python manage runserver
```

### Internacionalização

Siga os passos abaixo para atualizar ou gerar novos arquivos de tradução:

```bash
# 1. Criar ou atualizar o arquivo django.po com traduções pendentes
$ python manage maketranslations
# 2. Atualizar django.po com as novas traduções (diretamente no arquivo)
# 3. Compilar django.po em django.mo
$ python manage compilemessages
```

### Minificando SVGs

Caso o mapa (SVG) necessite ser atualizado, é importante que ele seja
minificado para diminuir o tamanho do arquivo final. Para isso, podemos
usar `svgo`:

```bash
$ npm install -g svgo
```

Minificando o arquivo:

```bash
$ svgo static/img/mapa.svg -o static/img/mapa.min.svg
```

## Deployment

```bash
$ ssh root@agropecuariaah.agr.br
$ cd /var/www/ahsite
$ git pull
$ pip install -r requirements/dev.txt
$ python manage.py migrate
$ python manage.py compilemessages
$ python manage.py collectstatic
$ service nginx restart && service gunicorn restart
```
