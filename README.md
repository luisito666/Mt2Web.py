 # Mt2Web.py

Web para servidores de Metin2.

## Motivación

La principal motivación que da surgimiento a este proyecto, es tener una web de Metin2 con los estándares actualizados, un código limpio y fácil de leer con alternativas para las donaciones (paymentwall).

## Caracteristicas principales.

1. Implementación de paymentwall para las donaciones.
2. Correo de activación.
3. Implementación de google re captcha en el registro login y recuperación de contraseña.
4. Recuperación de contraseña via email.
5. Panel de administración.
6. Analizador de base de datos.
7. Top de jugadores con crontab - (aliviana carga de la pagina y el juego).

## Requerimientos

1. Python 3.5
2. pip
3. Virtualenv
4. Git
5. Servidor web Apache o nginx

## Instalación.

Los comandos de instalación son los siguientes.

```
pip install virtualenv
virtualenv miweb
cd miweb/
source bin/activate
git clone https://github.com/luisito666/Mt2Web.py.git
cd Mt2Web.py/
pip install -r requirements.txt
```

1. Instala el paquete virtualenv de Python.
2. Crea un entorno virtual llamado miweb.
3. Ingresa al directorio.
4. Activar el entorno virtual.
5. Clona el repositorio de github.
6. Ingresa el directorio del proyecto.
7. Instala las dependencias del proyecto.

Con esto, se finaliza la Instalacion del proyecto. Ahora, hay que alistar el archivo de configuracion, en este archivo definiremos la conexion a la base de datos y otros aspectos importantes del funcionamiento.


Se crea un archivo de nombre settings.py en el directorio llamado core, editamos el archivo colocando el siguiente código:

```

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #librerias de Terceros
    'captcha',
    'bootstrapform',
    'corsheaders',
    #aplicaciones
    'apps.varios',
    'apps.account',
    'apps.player',
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
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
# Configuracion de la base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_metin2',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '3306',
        'OPTIONS': {
		            'init_command': "SET GLOBAL event_scheduler = ON",
		            'init_command': querys.event_top,
					},
    },
    'player': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'player',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '3306',
    },
    'account': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'account',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '3306',
        'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",},
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'

#Nombre del servidor.
SERVERNAME = 'Metin2 XxX'

#URL del servidor.
#Se usa para crear urls manuales. incluir el protocolo ejemplo http://tudominio.com o
#   https://tudominio.com
SERVERURL = 'http://127.0.0.1:8000'

#Llaves del recapcha
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''

#Llaves del paymentwall
PAYMENTWALL_PUBLIC_KEY = ''
PAYMENTWALL_PRIVATE_KEY = ''

#Configuracion del recapcha no tocar
NOCAPTCHA = True

#Configuracion files entorno de desarrollo no tocar
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),    
]

#configuraciones de correo
EMAIL_USE_TLS = True
EMAIL_HOST = ''
EMAIL_PORT = 25
EMAIL_HOST_USER = 'no_reply@tudominio.com'
EMAIL_HOST_PASSWORD = '****'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#Configuracion de duracion de buff
#Con esta configuracion al momento del registro se definira la duracion de los buff
#Por defecto se vencen el 2020
BUFFSTUF = '2020-01-01T00:00:00'

#Configuracion de la fecha de activacion.
#Con esta configuracion se definira desde que fecha esta disponible la cuenta.
#* Adelantar la fecha 2 años a partir del año en el que se encuentren, en caso
#  de tener activado el email de activacion.
#* Atrazarlo un año en caso de no usar email de actiacion y la cuenta quede
#  activada al momento del registro
ACTIVATE = '2020-01-01T00:00:00'

```

Despues de lo anterior se ejecutan las migraciones.

```
cd miweb
source bin/activate
cd Mt2Web.py/
./manage.py migrate
```

Continuamos agregando un campo extra a la base de datos, esto para que el aplicativo funcione correctamente.

Ejecutar desde el navicat el siguiente query

```
alter table account.account add column token_expire DATETIME null

```

## Entorno de pruebas.

Para trabajar con el entorno de pruebas, y mirar como es la web sin necesidad de instalar el servidor web.
Tener en cuenta que este servidor soporta muy pocos usuario y no sirve para un entorno de produccion

Estando en el directorio miweb

```
source bin/activate
cd Mt2Web.py/
./manage.py runserver
```

El server de pruebas queda ejecutandose localmente.
La url es http://127.0.0.1:8000/

## Crear super usuario

El super usuario sirve para entrar a la interface de administraicon del proyecto, en ese lugar podras realizar tareas administrativas, tambien podras supervisar cuales usuarios han realizando donaciones mediante paymentwall

```
./manage.py createsuperuser
```
La url de la interface de administracion es.
http://tudominio.com/admin
