# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# import de datetime nativo de python
import datetime

# Django imports
from django.views import View
from django.shortcuts import render

# Importando los modelos a usar
from apps.account.models import Account

# Importando los formularios a usar
from apps.account.forms import FormRequestPassword

# importando funciones
from apps.account.funciones import lenguaje, get_mail_username

# importando excepciones
from apps.account.excepciones import SendMailException

# importando libreria para enviar correo
from django.core.mail import send_mail

# importando las configuracines de django
from core import settings

# traducciones
from django.utils.translation import ugettext as _

class RequestUsername(View):
    template_name = 'account/request_username.html'
    model = Account
    form = FormRequestPassword

    def get(self, request):
        lenguaje(request)
        form = self.form(request.POST or None)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        lenguaje(request)
        form = self.form(request.POST or None)
        context = {
            'form': form
        }
        if form.is_valid():
            accounts = Account.objects.filter(email=form.cleaned_data['email'])
            if len(accounts) == 0:
                context.update({
                    'key': _('No se encontraron cuentas asociadas al email')
                })
                return render(request, self.template_name, context)
            try:
                send_mail(
                    _('Cuentas asociadas al correo ') + settings.SERVERNAME,
                    'content',
                    settings.EMAIL_HOST_USER,
                    [form.cleaned_data['email']],
                    html_message=get_mail_username(accounts)
                )
            except SendMailException as err:
                context.update({'err': err})
                return render(request, self.template_name, context)
            context.update({
                'key': _('Correo enviado exitosamente')
            })
            return render(request, self.template_name, context)

        else:
            return render(request, self.template_name, context)

