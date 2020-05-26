# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# Django
from django.shortcuts import render, redirect
from django.views import View

# Models
from apps.account.models import Account
from apps.varios.models import Top

# forms
from apps.account.forms import CustomDesbugForm

# utils
from apps.account.funciones import cambio_mapa

# translation
from django.utils.translation import ugettext as _


class UnlockPlayer(View):
    model_account = Account
    model_player = Top
    template_name = 'account/unlock_player.html'
    form_class = CustomDesbugForm

    def get(self, request):
        if 'g1jwvO' in request.session:
            context = {'form': self.form_class()}
            players = self.model_player.objects.filter(account_id=request.session['g1jwvO'])
            if players.count() == 0:
                return redirect('account:login')
            context.update({
                'if_form': True,
                'form': self.form_class
            })
            return render(request, self.template_name, context)        
        else:
            return redirect('account:login')

    def post(self, request):
        if 'g1jwvO' in request.session:
            form = self.form_class( request.POST or None )
            context = {'form': form}
            if form.is_valid():
                player = form.cleaned_data['nombre']
                players = self.model_player.objects.filter(account_id=request.account.id)
                for pj in players:
                    if str.lower(pj.name) == str.lower(player):
                        change_map = cambio_mapa(request.account.id, pj.name)
                        if change_map:
                            context.update({
                            'key': _('Se ha movido tu personaje correctamente debes esperar '
                                     '30 min para iniciar con el.'),
                            'if_form': True
                            })
                            return render(request, self.template_name, context)
                        else:
                            context.update({
                            'key': _('Error moviendo personaje'),
                            'if_form': True
                            })
                            return render(request, self.template_name, context)
                context.update({
                'key': _('Ningun personaje coincide.'),
                'if_form': True
                })
                return render(request, self.template_name, context)
        else:
            return redirect('account:login')

