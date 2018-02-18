# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

from django.shortcuts import render, redirect
from apps.account.funciones import *
from apps.account.payview import PayWidget
from core import settings
from apps.account import models

def index(request):
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
