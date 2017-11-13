from django.shortcuts import render, redirect
from apps.account.funciones import *
from apps.account.payview import PayWidget, ProcessPay
from core import settings
from apps.account import models

def index(request):
	context = {
			'servername': settings.SERVERNAME,
			'player': total_pl(),
			'account': total_us(),
			'online': last_hour(),
			'actualmente': last_min(),
			'top_player': player_top(),
			'guild_top': guild_top()
	}
	return render(request, 'index.html', context)

def donaciones(request):
	if request.session.has_key('id'):
		try:
			a = models.Account.objects.get(id=request.session['id'])
		except Account.DoesNotExist:
			pass

		widget = PayWidget(a.login,a.email)
		context = {
				'widget':widget,
				'servername': settings.SERVERNAME,
				'player': total_pl(),
				'account': total_us(),
				'online': last_hour(),
				'actualmente': last_min(),
				'top_player': player_top(),
				'guild_top': guild_top()
		}
		return render(request, 'donaciones.html', context)
	else:
		return redirect('account:login')

def payproces(request):
	context = ProcessPay(request)
	return render(request, 'donaciones.html', context)
