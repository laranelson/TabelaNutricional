import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'smalh&4&k&ubv%-ijsrgh0$tnvf%+dubsl83(h2!l4j)&%fi9&'

# The `DYNO` env var is set on Heroku CI, but it's not a real Heroku app, so we have to
# also explicitly exclude CI:
# https://devcenter.heroku.com/articles/heroku-ci#immutable-environment-variables
IS_HEROKU_APP = "DYNO" in os.environ and not "CI" in os.environ


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if IS_HEROKU_APP:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
     # Use WhiteNoise's runserver implementation instead of the Django default, for dev-prod parity.
    "whitenoise.runserver_nostatic",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'core',
    'crispy_forms',
    "crispy_bootstrap4",
    'recipe',
    'ingredient',
    'table',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



ROOT_URLCONF = 'inlineformset.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'inlineformset.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

#DATABASES = {
#    'default': {
#       'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

#DATABASE_HEROKU
DATABASES= {
    'default': dj_database_url.config()
}

#prod_db  =  dj_database_url.config(conn_max_age=500)
#DATABASES['default'].update(prod_db)

#BASE DE DADOS LOCAL
"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db-nutritiontable',
        'USER': 'postgres',
        'PASSWORD': 'n3140n',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}"""

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

#COMENTAR STATIC_URL QUANDO FOR FAZER DEPLOY
STATIC_URL = '/static/'

# Definição do diretório raiz do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# DEVE SER LIBERADO PARA DEPLOY
# Definição do diretório raiz do projeto para os arquivos estáticos
#PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Definição do diretório onde os arquivos estáticos serão coletados em produção
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# DEVE SER LIBERADO PARA DEPLOY
# Definição do diretório onde o Django procura por arquivos estáticos durante o desenvolvimento
#STATICFILES_DIRS = (
#    os.path.join(PROJECT_ROOT, 'static'),
#)

# Importe o tipo de campo BigAutoField
from django.db.models import BigAutoField

# Defina DEFAULT_AUTO_FIELD para BigAutoField
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Define a URL para a qual o usuário será redirecionado após o logout
LOGOUT_REDIRECT_URL = 'index'

# Especifica o conjunto de templates do Crispy Forms a ser usado, neste caso, o Bootstrap 4
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Permite explicitamente apenas o uso do conjunto de templates do Crispy Forms para o Bootstrap 4
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"

# Define o armazenamento de arquivos estáticos usando whitenoise para compressão e manifestação
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Desabilita a execução do comando 'collectstatic' automaticamente durante o deploy
DISABLE_COLLECTSTATIC = 1


# Define o backend de e-mail a ser usado como SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Define o host do servidor SMTP, no caso do Gmail
EMAIL_HOST = 'smtp.gmail.com'

# Define a porta usada para a conexão SMTP com o Gmail
EMAIL_PORT = 587

# Especifica o uso do TLS (Transport Layer Security) para conexão segura
EMAIL_USE_TLS = True

# Insira seu endereço de e-mail completo do Gmail para autenticação
EMAIL_HOST_USER = "nelsonlarajr@gmail.com"  # Substitua com seu e-mail completo

# Insira a senha específica gerada pelo Google para aplicativos de terceiros
EMAIL_HOST_PASSWORD = "wlbgabslyyfckakn"  # Substitua com a senha gerada pelo Google
