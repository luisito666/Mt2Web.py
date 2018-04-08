# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

#importaciones por defecto de django
from django.shortcuts import render, redirect

#importaciones para el soporte multi idioma
from django.utils import translation
from django.utils.translation import ugettext as _

from apps.account.funciones import *
from apps.account.payview import PayWidget
from core import settings
from apps.account import models

def index(request):
	#Generando la variable de session que contendra el idioma usado
	if 'lang' in request.GET:
		for lang in settings.LANG_AVILABLE:
			if lang == request.GET.get('lang'):
				request.session['lang'] = request.GET.get('lang')
				break
			elif request.GET.get('lang') == 'default':
				if request.session.has_key('lang'):
					del request.session['lang']
					break

	#Cargando idioma definido
	if request.session.has_key('lang'):
		translation.activate(request.session['lang'])

	context = contexto()
	context.update({
		'key':_('New messages')
	})
	return render(request, 'index.html', contexto())

def donaciones(request):
	if request.session.has_key('g1jwvO'):
		try:
			a = models.Account.objects.get(id=request.session['g1jwvO'])
		except Account.DoesNotExist:
			pass

		widget = PayWidget(a.login,a.email)
		context = contexto()
		context.update({
				'widget':widget,
				'session': a ,
		})
		return render(request, 'donaciones.html', context)
	else:
		return redirect('account:login')
