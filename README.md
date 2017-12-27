# Mt2Web.py

Web para servidores de Metin2.

## Motivacion

La motivacion principal para realizar este proyecto, es tener una web de metin2 con los estandares actualizado, ademas de un codigo limpio y facil de leer, tambien tener una alternativa para implementar las donaciones mediante Paymentwall.

## Caracteristicas principales.

1. Implementacion de paymentwall para las donaciones
2. Correo de activacion
3. Implementacion de google re captcha en el registro login y recuperacion de contraseña
4. Recuperacion de contraseña via email
5. Panel de administracion
6. Analizador de base de datos.
7. Top de jugadore con crontab - aliviana carga de la pagina y el juego

## Requerimientos

1. Python 3.5
2. pip
3. Virtualenv
4. Git
5. Servidor web Apache o nginx

## Instalacion.

Los comandos para instalar son los siguientes.

```
pip install virtualenv
virtualenv miweb
cd miweb/
source bin/activate
git clone https://github.com/luisito666/Mt2Web.py.git
cd Mt2Web.py/
pip install -r requirements.txt
```

1. instala el paquete virtualenv de Python
2. crea un entorno virtual llamado miweb
3. ingresa al directorio
4. activar el entorno virtual
5. clona el repositorio de github
6. ingresa el directorio del proyecto
7. instalan las dependencias del proyecto

Ya con eso finalizamos la Instalacion del proyecto, ahora hay que alistar el archivo de configuracion, en este archivo definiremos la conexion a la base de datos y otros aspectos importantes del funcionamiento del proyecto.

Se copia el archivo de configuracion que aparece descrito en la parte inferior, este archivo se pone en el directorio core, con el nombre de settings.py

Se tiene que configurar los datos de conexion a mysql

```

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wye8(vj+&1s(g(%bh_3=aw4h@w5&nwgl9ar4x5p6+n0i*&tl8t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1']


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
#STATIC_ROOT = '/home/zaunt/static'

#Nombre del servidor.
SERVERNAME = 'Metin2 XxX'

#URL del servidor.
"""Se usa para crear urls manuales. incluir el protocolo ejemplo http://tudominio.com o
   https://tudominio.com
"""
#Pruebas
#SERVERURL = 'http://127.0.0.1:8000'

#Produccion
SERVERURL = ''

#Configuracion del recapcha
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''

#configuracion del paymentwall
PAYMENTWALL_PUBLIC_KEY = ''
PAYMENTWALL_PRIVATE_KEY = ''

#No Tocar
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
```

Despues de lo anterior se ejecutan las migraciones.

```
cd miweb
source bin/activate
cd Mt2Web.py/
./manage.py migrate
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
