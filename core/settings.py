
import os
import yaml
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Cargando la configuracion del proyecto
CONFIG = yaml.load(open(BASE_DIR + '/config.yml').read())

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_random_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#DEBUG = False

ALLOWED_HOSTS = ['localhost', CONFIG['server']['domain'], 'www.' + CONFIG['server']['domain'] ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # librerias de Terceros
    'captcha',
    'bootstrapform',
    'corsheaders',
    'rest_framework',
    # aplicaciones
    'apps.account',
    'apps.player',
    'apps.varios',
    'apps.paginas',
    'apps.api',
    'apps.administracion.estadisticas',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'apps.account.middleware.AccountMiddleware'
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.applist.applist',
                'apps.account.funciones.contexto',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
# Configuracion de la base de datos
DATABASES = {
    'account': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'account',
        'USER': CONFIG['database']['user'],
        'PASSWORD': CONFIG['database']['password'],
        'HOST': CONFIG['database']['host'],
        'PORT': CONFIG['database']['port'],
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES';",
        },
    },
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_metin2',
        'USER': CONFIG['database']['user'],
        'PASSWORD': CONFIG['database']['password'],
        'HOST': CONFIG['database']['host'],
        'PORT': CONFIG['database']['port'],
        'OPTIONS': {},
    },
    'player': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'player',
        'USER': CONFIG['database']['user'],
        'PASSWORD': CONFIG['database']['password'],
        'HOST': CONFIG['database']['host'],
        'PORT': CONFIG['database']['port'],
        'OPTIONS': {
            'init_command': "CREATE DATABASE IF NOT EXISTS django_metin2;" ,
        },
    },
}

DATABASE_ROUTERS = {
    'apps.player.router.playerRouter',
    'apps.account.router.AccountRouter',
}
# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = CONFIG['server']['timezone']

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'

# Nombre del servidor.
SERVERNAME = CONFIG['server']['name']

# URL del servidor.
# Se usa para crear urls manuales. incluir el protocolo ejemplo http://tudominio.com o
#   https://tudominio.com
SERVERURL = CONFIG['server']['url']

# habilitar y deshabilitar Recapcha
RECAPTCHA = CONFIG['captcha']['enable']

# Llaves del recapcha
RECAPTCHA_PUBLIC_KEY = CONFIG['captcha']['public_key']
RECAPTCHA_PRIVATE_KEY = CONFIG['captcha']['private_key']

# Llaves del paymentwall
PAYMENTWALL_PUBLIC_KEY = CONFIG['paymentwall']['public_key']
PAYMENTWALL_PRIVATE_KEY = CONFIG['paymentwall']['private_key']

# Configuracion del recapcha no tocar
NOCAPTCHA = True

# Configurando directorio que contiene las traducciones
# Por favor no tocar
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

LANG_AVILABLE = ['en']

# Configuracion files entorno de desarrollo no tocar
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),    
]

# Configuraciones de correo
EMAIL_USE_TLS = True
EMAIL_HOST = CONFIG['mail']['host']
EMAIL_PORT = CONFIG['mail']['port']
EMAIL_HOST_USER = CONFIG['mail']['user']
EMAIL_HOST_PASSWORD = CONFIG['mail']['password']
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Configuracion de duracion de buff
# Con esta configuracion al momento del registro se definira la duracion de los buff
# Por defecto se vencen el 2020

BUFFSTUF = '2018-08-13T00:00:00'

FINALSTUFF = '2020-01-01T00:00:00'

# Configuracion de la fecha de activacion.
# Con esta configuracion se definira desde que fecha esta disponible la cuenta.
# 1. Adelantar la fecha 2 años a partir del año en el que se encuentren, en caso
# de tener activado el email de activacion.
# 2. Atrazarlo un año en caso de no usar email de actiacion y la cuenta quede
# activada al momento del registro
if CONFIG['register']['mail_activate_account']:
    ACTIVATE = '2025-01-01T00:00:00'
else:
    ACTIVATE = '2009-01-01T00:00:00'


CORS_ORIGIN_WHITELIST = (
    'google.com',
    'hostname.example.com',
    'localhost:8000',
    '127.0.0.1:9000',
    '*'
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.api.authentication.TokenAuthentication',
    )
}