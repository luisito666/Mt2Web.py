# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# Django Imports
from django.views import View
from django.shortcuts import render, redirect

# importando forms
from apps.account.forms import CustomLoginForm

# importando models
#from apps.account.models import Account
from apps.authentication.models import Account
from apps.varios.models import Top

# importando funciones
from apps.account.funciones import lenguaje

# traducciones
from django.utils.translation import ugettext as _


class Login(View):

    template_name = 'account/login.html'
    template_name_login = 'account/logon.html'
    modelA = Account
    modelB = Top
    form = CustomLoginForm

    def get(self, request):
        lenguaje(request)
        form = self.form()

        if 'g1jwvO' in request.session:
        #if request.account.is_authenticated:
            userinfo = self.modelA.objects.get(id=request.session['g1jwvO'])
            pjinfo = self.modelB.objects.filter(account_id=userinfo.id)
            context = {
                'session': userinfo,
                'personajes': pjinfo
            }
            return render(request, self.template_name_login, context)
        else:
            pass

        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        lenguaje(request)
        form = self.form(request.POST or None)

        if form.is_valid():
            from apps.authentication import login
            login(request, )

        else:
            context = {
                'key': _('Rellene todos los campos correctamente'),
                'form': form
            }
            return render(request, self.template_name, context)

