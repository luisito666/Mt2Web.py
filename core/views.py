from django.shortcuts import render, redirect
from apps.account.funciones import *
from apps.account.payview import PayWidget
from core import settings
from apps.account import models

def index(request):
	return render(request, 'index.html', contexto())

def donaciones(request):
	if request.session.has_key('id'):
		try:
			a = models.Account.objects.get(id=request.session['id'])
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
