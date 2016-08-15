# -*- coding: utf-8 -*-
import os

# Django settings for maximize project.
DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = True

ADMINS = (
    # ('Luiz Felipe', 'luiz_anao@hotmail.com'),
)

MANAGERS = ADMINS
APP_PATH = '/home/luizfelipe/Dropbox/django/torinvestimentos/'
# APP_PATH = "/home/luizfelipe/torinvestimentos/" # os.getcwd()
# APP_PATH = '/home/maximize/webapps/django/myproject' #os.getcwd()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'torinvestimentos',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '123',               # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-br'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = APP_PATH + '/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL =  '/media/'



# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'px=f8b5gu=2(kmhkh)x8ht+bk#ziekz-z5!c2i!$g%j@$8g#$t'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    APP_PATH + '/templates/'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    #'grappelli',
    # 'mailer',
    # 'sorl.thumbnail',
    'django.contrib.admin',
    # 'haystack',
    'app',
    # 'django_evolution'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth", 
    "django.core.context_processors.debug", 
    "django.core.context_processors.i18n", 
    "django.core.context_processors.media", 
    'django.core.context_processors.request',
)

THUMBNAIL_PROCESSORS = (
    'sorl.thumbnail.processors.colorspace',
    'sorl.thumbnail.processors.autocrop',
    'sorl.thumbnail.processors.scale_and_crop',
    'sorl.thumbnail.processors.filters',
    # 'app.processors.pad',
)

UPLOADS_ROOT = APP_PATH + '/media/uploads/'

# Lista de Paginas 
PAGINAS_CHOICES = (
    ('pagina_inicial', u'Página Inicial'),
    ('quem_somos', u'Quem Somos'),
    ('noticias', u'Notícias'),
    ('produtos', u'Produtos'),
    ('servicos', u'Serviços'),
    ('clientes', u'Clientes'),
    ('contato', u'Contato'),
)

# Haystack
# HAYSTACK_SITECONF = 'torinvestimentos.search_sites'
# HAYSTACK_SEARCH_ENGINE = 'whoosh'
# HAYSTACK_WHOOSH_PATH = APP_PATH + '/search_index'


# Lista de Estados
ESTADO_CHOICES = (
    ('AC', 'AC - Acre'),
    ('AL', 'AL - Alagoas'),
    ('AM', 'AM - Amazonas'),
    ('AP', 'AP - Amapá'),
    ('BA', 'BA - Bahia'),
    ('CE', 'CE - Ceará'),
    ('DF', 'DF - Distrito Federal'),
    ('ES', 'ES - Espírito Santo'),
    ('GO', 'GO - Goiás'),
    ('MA', 'MA - Maranhão'),
    ('MG', 'MG - Minas Gerais'),
    ('MS', 'MS - Mato Grosso do Sul'),
    ('MT', 'MT - Mato Grosso'),
    ('PA', 'PA - Pará'),
    ('PB', 'PB - Paraíba'),
    ('PE', 'PE - Pernambuco'),
    ('PI', 'PI - Piauí'),
    ('PR', 'PR - Paraná'),
    ('RJ', 'RJ - Rio de Janeiro'),
    ('RN', 'RN - Rio Grande do Norte'),
    ('RO', 'RO - Rondônia'),
    ('RR', 'RR - Roraima'),
    ('RS', 'RS - Rio Grande do Sul'),
    ('SC', 'SC - Santa Catarina'),
    ('SE', 'SE - Sergipe'),
    ('SP', 'SP - São Paulo'),
    ('TO', 'TO - Tocantins')
)

# Quantidade máxima de Imagens por tipo de Página
MAX = {
    "Produto": {"ImagemInline": 4, "AnexoInline": 2},
    "Servico": {"ImagemInline": 4, "AnexoInline": 2},
    "Cliente": {"ImagemInline": 4, "AnexoInline": 2},
    "Noticia": {"ImagemInline": 6, "AnexoInline": 2},
    "Pagina":  {"ImagemInline": 6, "AnexoInline": 2},
}

# Configurações para envio de e-mail
EMAIL_HOST = ""
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
