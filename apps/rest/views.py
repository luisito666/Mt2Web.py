#Importando Serializadores Nativos
from apps.rest.serializers import AccountSerializer, SerializersTop, SerializersGuild, \
								  SerializersDescargas, SerializersGremios, RegisterSerializers

#importando libreria para enviar correo
from django.core.mail import send_mail

#Importando Modelos
from apps.account.models import Account
from apps.varios.models import Top, Descarga
from django.db.models import Q

#importando paginadores
from .pagination import PostPageNumber

#importando utilidades
from apps.account.funciones import *

#Importando del rest Framework
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

#importando las configuracines de django
from zaunt import settings


@api_view(['GET'])
def UsersDetail(request,login):

	respuesta_error = {'status':'error', 'data':'Usuario no existe'}

	if request.method == 'GET':
		try:
			queryset = Account.objects.get(login=login)
		except:
			return Response(respuesta_error)

		data = AccountSerializer(queryset)
		respuesta_ok = {'status':'OK', 'data': data.data}
		return Response(respuesta_ok)

@api_view(['GET'])
def StatsDetail(request):

	if request.method == 'GET':
		response = {
			'status': 'OK',
			'data': {
			'online': last_min(),
			'registros': total_us(),
			'personajes': total_pl(),
			'venticuatro': last_hour()
			}
		}

		return Response(response)


@api_view(['GET'])
def Ranking(request):

	if request.method == 'GET':
		jugadores = player_top()
		serializers = SerializersTop(jugadores, many=True)
		data = {'status':'OK', 'data': serializers.data }
		return Response(data)


@api_view(['GET'])
def RankingGremios(request):

	if request.method == 'GET':
		gremios = guild_top()
		serializers = SerializersGuild(gremios, many=True)
		data = {'status':'OK', 'data': serializers.data }
		return Response(data)

@api_view(['GET'])
def Descargas(request):
	if request.method == 'GET':
		queryset = Descarga.objects.all()
		serializers = SerializersDescargas(queryset, many=True)
		data = {'status':'OK', 'data': serializers.data }
		return Response(data)

class TopList(generics.ListAPIView):
	queryset = Top.objects.all().exclude(Q(name__contains='[')).order_by('-level','-exp')
	serializer_class = SerializersTop
	pagination_class = PostPageNumber


class GuidList(generics.ListAPIView):
	queryset = Guild.objects.all().order_by('-level','-exp','-win', '-ladder_point')
	serializer_class = SerializersGremios
	pagination_class = PostPageNumber

class RegisterApi(APIView):

	def get(self, request):
		return Response({'status':'Nada que mostrar.'})

	def post(self, request, format=None):
		serializer = RegisterSerializers(data = request.data)
		if serializer.is_valid():
			serializer.save()
			key = aleatorio(40)
			try:
				a = Account.objects.get(login=serializer.data['login'])
			except:
				return Response({'status':'error obteniendo data de la cuenta'})

			a.address = key
			a.save()
			try:
				send_mail(
					'Bienvenido Metin2 Zaunt',
					'Content',
					settings.EMAIL_HOST_USER ,
					[a.email], 
					html_message=get_mail_register(a.login,key),
					)
				return Response(serializer.data)
			except:
				pass
		return Response(serializer.errors)