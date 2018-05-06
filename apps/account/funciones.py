# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

#importando  modelos necesarios
from apps.account.models import Account
from apps.player.models import Player
from apps.player.models import Guild
from apps.varios.models import Top
from django.db.models import Q

#importando clase usada para la traduccion
from django.utils import translation

#importando funciones del framework
from django.db import connections
from django.utils import timezone

#importando configuraciones del proyecto
from core import settings

#Esta funcion se usa para ver la clasificacion de gremios
def guild_top(cantidad=None):
	#Cantidad tiene que se un numero.
	if cantidad:
		return Guild.objects.all().order_by('-level','-exp','-win', '-ladder_point')[:cantidad]
	return Guild.objects.all().order_by('-level','-exp','-win', '-ladder_point')

#Esta funcion se usa para mostrar la clasificacion del jugadores
def player_top(cantidad=None):
	#Cantidad tiene que ser un numero.
	if cantidad:
		return Top.objects.all().exclude(Q(name__contains='[')).order_by('-level','-ranking')[:cantidad]
	return Top.objects.all().exclude(Q(name__contains='[')).order_by('-level','-ranking')

#Esta funcion es para ver cuantas cuentas tiene el server
def total_us():
	a = Account.objects.all().count()
	return a

#Esta funcion es para ver cuantos player hay en el server
def total_pl():
	a = Player.objects.all().count()
	return a

#Esta funcion es para ver cuantas personas hay online
def last_min():
	cursor = connections['player'].cursor()
	cursor.execute("SELECT COUNT(*) as count FROM player WHERE DATE_SUB(NOW(), INTERVAL 5 MINUTE) < last_play")
	a = cursor.fetchall()
	b = a[0][0]
	return b

#Esta funcion es para ver cuantos jugadores en promedio hay en las ultimas 24 horas
def last_hour():
	cursor = connections['player'].cursor()
	cursor.execute("SELECT COUNT(*) as count FROM player WHERE DATE_SUB(NOW(), INTERVAL 24 HOUR) < last_play")
	a = cursor.fetchall()
	b = a[0][0]
	return b

#Esta funcion genera password aleatorios
def aleatorio(longitud):
	#importando modulo de python
	from random import SystemRandom

	#definiendo caracteres a usar
	valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

	cryptogen = SystemRandom()
	password = ""

	#generando password aleatorio
	while longitud > 0:
	  password = password + cryptogen.choice(valores)
	  longitud = longitud - 1

	return password

#Funcion usada para retornar el texto del correo de recuperacion de contrasena
def get_mail(nombre, key):
	mensaje ='<h3> Hola %s </h3>' % nombre
	mensaje+='<p>has solicitado un email para recuperar el password </p>'
	mensaje+='<p>para proceder usa el siguiente <a href="' + settings.SERVERURL + '/password/%s">link</a> </p>' % key
	mensaje+='<p>si no has solicitado el dicho cambio ignorar este correo </p>'
	mensaje+='<p> Att: Staff <strong>' + settings.SERVERNAME + '</strong> </p>'
	return mensaje

#Funcion usada para retornar el texto de correo de bienvenida al juego
def get_mail_register(cuenta, key):
	mensaje = '<h3> Bienvenido a ' + settings.SERVERNAME + '. </h3>'
	mensaje+= '<p>Por favor guarda este email para futuras referencias. La informacion de tu'
	mensaje+= ' cuenta es la siguiente:</p>'
	mensaje+= '----------------------------'
	mensaje+= '<p>Nombre de usuario: %s </p>' % cuenta
	mensaje+= '<p>URL del Sitio: ' + settings.SERVERURL + ' <p>'
	mensaje+= '----------------------------'
	mensaje+= '<p>Usa el siguiente link para activar tu cuenta: <a href="' + settings.SERVERURL + '/activar/%s"> Activar </a> </p>' % key
	mensaje+= '----------------------------'
	mensaje+= '<p>Tu clave ha sido encriptada en nuestra base de datos. Si la olvidaste'
	mensaje+= 'podras solicitar una nueva la cual sera activada en la misma forma que esta '
	mensaje+= 'cuenta. </p>'
	mensaje+= '<p> Gracias por registrarte. </p>'
	mensaje+= '--'
	mensaje+= '<p>Att: Staff ' + settings.SERVERNAME + ' </p>'
	return mensaje

#Funcion usada para cambiar de mapa a un personaje
def cambio_mapa(cuenta, personaje):
	sql = "UPDATE player SET x=436377, y=215769, map_index=61, exit_x=436378, exit_y=215769, exit_map_index=61 WHERE name='%s' AND account_id='%s' " % ( personaje, cuenta )
	cursor = connections['player'].cursor()
	a = cursor.execute( sql )
	cursor.fetchall()
	return a

#Funcion usada para manejar el contexto del proyecto
def contexto(request):
	return {
		'servername': settings.SERVERNAME,
		'player': total_pl(),
		'account': total_us(),
		'online': last_hour(),
		'actualmente': last_min(),
		'top_player': player_top(5),
		'guild_top': guild_top(5)
	}

#funcion usada para activar las traducciones
def lenguaje(request):
	if request.session.has_key('lang'):
		translation.activate(request.session['lang'])
