# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# Django Imports
from django.shortcuts import render, redirect
from django.views import View

# importando forms
from apps.account.forms import CustomChangePassword

# importando models
from apps.account.models import Account
from apps.varios.models import Top

# importando funciones
from apps.account.funciones import lenguaje

# traducciones
from django.utils.translation import ugettext as _

class ResetPassword(View):
    template_name = 'account/reset_password.html'
    form = CustomChangePassword
    model = Account

    def get(self, request):
        lenguaje(request)
        context = {'form': self.form}
        if 'g1jwvO' in request.session:
            return render(request, self.template_name, context)
        else:
            return redirect('account:login')

    def post(self, request):
        lenguaje(request)
        form = self.form(request.POST)
        context = {'form': form }
        if 'g1jwvO' in request.session:
            try:
                account = Account.objects.get(id=request.session['g1jwvO'])
            except Account.DoesNotExist:
                raise 'Invalid session'

            if request.POST['new_password'] == request.POST['new_password_again']:
                if form.is_valid():
                    if account.validate_password(form.cleaned_data['password']):
                        account.update_password(form.cleaned_data['new_password'])
                        account.save()

                        context.update({'key': _('se ha cambiado el password exitosamente.')})
                        return render(request, self.template_name, context)
                    else:
                        context.update({'key': _('El password no es correcto')})
                        return render(request, self.template_name, context)
            else:
                # contraseas no coinciden
                context.update({'key': _('Los password no coinciden')})
                return render(request, self.template_name, context)

        
        else:
            return redirect('account:login')
