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
from apps.account.forms import ResPassword

# importando funciones
from apps.account.funciones import lenguaje

# Clase usada para re enviar el correo de activacion, en caso de que no llegue.
class RequestToken(View):

    template_name = 'account/request_token.html'
    model = Account
    form = ResPassword

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
            try:
                a = self.model.objects.get(login=form.cleaned_data['login'])
            except Account.DoesNotExist:
                context.update({
                    'key': _('Cuenta no existe.')
                })
                return render(request, self.template_name, context)

            b = datetime.datetime(2009, 1, 1, 0, 0,)
            if a.availdt.year == b.year and a.availdt.month == b.month:
                context.update({
                    'key': _('Tu cuenta ya esta activada'),
                })
                return render(request, self.template_name, context)

            if a.status != 'OK':
                context.update({
                    'key': _('Tu cuenta esta baneada')
                })
                return render(request, self.template_name, context)

            if form.cleaned_data['email'] == a.email:
                key = aleatorio(40)
                a.address = key
                a.save()
                try:
                    send_mail(
                        _('Activacion de cuentas ')+settings.SERVERNAME,
                        'Content',
                        settings.EMAIL_HOST_USER,
                        [a.email],
                        html_message=get_mail_register(a.login, key)
                    )
                except SendMailException:
                    context.update({
                        'key': _('Error enviando correo al usuario')
                    })
                    return render(request, self.template_name, context)

                context.update({
                    'key': _('Se ha enviado el codigo de activacion al email')
                })
                return render(request, self.template_name, context)
            else:
                context.update({
                    'key': _('El email no coincide con el usuario')
                })
                return render(request, self.template_name, context)
        else:
            context.update({
                'key': _('Por favor rellena todos los campos correctamente.')
            })
            return render(request, self.template_name, context)

