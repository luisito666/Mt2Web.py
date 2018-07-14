# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# importaciones por defecto de django
from django.shortcuts import render, redirect

# Importaciones para el soporte multi idioma
from django.utils import translation
from apps.account.funciones import lenguaje
# from django.utils.translation import ugettext as _

from apps.account.payview import PayWidget
from core import settings
from apps.account.models import Account


def index(request):
    # Generando la variable de session que contendra el idioma usado
    if 'lang' in request.GET:
        for lang in settings.LANG_AVILABLE:
            if lang == request.GET.get('lang'):
                request.session['lang'] = request.GET.get('lang')
                break
            elif request.GET.get('lang') == 'default':
                request.session['lang'] = 'default'
                break

    # Cargando idioma definido
    if 'lang' in request.session:
        translation.activate(request.session['lang'])

    return render(request, 'index.html')


def donaciones(request):
    lenguaje(request)
    if 'g1jwvO' in request.session:
        try:
            a = Account.objects.get(id=request.session['g1jwvO'])
        except Account.DoesNotExist:
            pass

        widget = PayWidget(a.login, a.email)
        context = {
            'widget': widget,
            'session': a,
        }
        return render(request, 'donaciones.html', context)
    else:
        return redirect('account:login')
