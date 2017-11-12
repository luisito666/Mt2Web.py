from django.shortcuts import render, redirect
from apps.account.funciones import *
from zaunt import settings


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
	context = {
			'servername': settings.SERVERNAME,
			'player': total_pl(),
			'account': total_us(),
			'online': last_hour(),
			'actualmente': last_min(),
			'top_player': player_top(),
			'guild_top': guild_top()
	}
	return render(request, 'donaciones.html', context)
