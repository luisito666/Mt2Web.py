 # Mt2Web.py

Web para servidores de Metin2.

## Motivación

La principal motivación que da surgimiento a este proyecto, es tener una web de Metin2 con los estándares actualizados, un código limpio y fácil de leer con alternativas para las donaciones (paymentwall).

## Caracteristicas principales.

1. Implementación de paymentwall para las donaciones.
2. Correo de activación.
3. Implementación de google re captcha.
4. Recuperación de contraseña via email.
5. Panel de administración.
6. Analizador de base de datos.
7. Top de jugadores con un Job de python - (aliviana carga de la pagina y el juego).

## Requerimientos

1. Python 3.5.0
2. Git


## Instalación.

Los comandos de instalación son los siguientes.

```
git clone https://github.com/luisito666/Mt2Web.py.git
cd Mt2Web.py/
python -m venv env3
source env3/bin/activate
pip install -r requirements.txt
```

1. Clona el repositorio de github.
2. Ingresa al directorio del repositorio que se clono.
3. Crea un entorno virtual llamado env3.
4. Activar el entorno virtual.
5. Instala las dependencias del proyecto.

Con esto, se finaliza la Instalacion del proyecto. Ahora, hay que alistar el archivo de configuracion, en este archivo definiremos la conexion a la base de datos y otros aspectos importantes del funcionamiento.
Para esto se edita el archivo config.yml este archivo es muy intuitivo.


```
database:
  user: root
  password: 
  host: 
  port: 3306
server:
  name: 'Metin2 XxX'
  url: 'https://www.example.com'
  domain: 'example.com'
  timezone: 'America/Bogota'
paymentwall:
  public_key: ''
  private_key: ''
captcha:
  enable: False
  public_key: ''
  private_key: ''
mail:
  host: 0.0.0.0
  port: 25
  password: 'tu_pasword'
  user: 'tu_usuario@example.com'
register:
  mail_activate_account: False
```

Despues de lo anterior se ejecutan las migraciones.

Nota: este comando crea las tablas que requiere este proyecto para su funcionamiento. 

```
python manage.py migrate
```

Continuamos agregando un campo extra a la base de datos, esto para que el aplicativo funcione correctamente.

Ejecutar siguiente query para agregar campos que requiere la aplicacion para poder funcionar.

```
alter table account.account add column token_expire DATETIME null;
alter table account.account add column refer_id INT null;

```

## Entorno de pruebas.

Para trabajar con el entorno de pruebas, y mirar como es la web sin necesidad de instalar el servidor web.
Tener en cuenta que este servidor soporta muy pocos usuario y no sirve para un entorno de produccion

Estando en el directorio miweb

```
python manage.py runserver
```

El server de pruebas queda ejecutandose localmente.
La url es http://localhost:8000/

## Crear super usuario

El super usuario sirve para entrar a la interface de administraicon del proyecto, en ese lugar podras realizar tareas administrativas, tambien podras supervisar cuales usuarios han realizando donaciones mediante paymentwall

```
python manage.py createsuperuser
```
La url de la interface de administracion es.
http://tudominio.com/admin

## Entorno de Produccion.

Para el entorno de produccion se cuenta con un proyecto que automatiza este <a href="https://github.com/luisito666/Mt2Web.py-docker" target="_blank">proceso</a>.

<a href="https://github.com/luisito666/Mt2Web.py-docker" target="_blank">Mt2Web.py-docker.</a>