# Copyright (c) 2017-2018 ferchoafta@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

#import de python
import datetime

#importaciones que realiza django por defecto
from django.shortcuts import render, redirect

#Importando los modelos a usar

from apps.administracion.estadisticas.models import registroConectados

from django.db.models import Q

#importando los formularios a usar
from apps.account.forms import  CreateUserForm, \
                                CustomLoginForm, \
                                CustomChangePassword,\
                                ResPassword, \
                                FormResetPassword,\
                                CustomDesbugForm



#importando funciones integradas en el framework
from django.views.generic import CreateView, DetailView, ListView
from django.views import View
from django.http import HttpResponseRedirect , HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone

#importando las configuracines de django
from core import settings


class getRegistroOn(ListView):
    title='Estadisticas'
    model = registroConectados
    template_name = 'inicio.html'
    queryset = model.objects.filter().order_by('-id')[:24]




    def has_permission(self, request):
        """
        Returns True if the given HttpRequest has permission to view
        *at least one* page in the admin site.
        """
        return request.user.is_active and request.user.is_staff

    def get_context_data(self, **kwargs):
        context = {
                # 'site_title': "Inicio",
                'title': self.title,
                'has_permission': self.has_permission(self.request),
                'opts': {'app_label': self.title}
            }

        context.update(super(getRegistroOn, self).get_context_data(**kwargs))


        return context

