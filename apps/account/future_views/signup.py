# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# Django Imports
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

# importando forms
from apps.authentication.forms import AccountCreationForm

# importando models
from apps.account.models import Account

# importando libreria para enviar correo
from django.core.mail import send_mail

# importando excepciones
from apps.account.excepciones import SendMailException

# importando funciones
from apps.account.funciones import lenguaje, aleatorio

# traducciones
from django.utils.translation import ugettext as _

# importando las configuracines de django
from core import settings


class SignUp(CreateView):
    success_url = reverse_lazy('account:exito')
    template_name = 'account/signup.html'
    model = Account
    form_class = AccountCreationForm

    def get(self, request):
        lenguaje(request)
        return super(SignUp, self).get(request)

    def post(self, request):
        lenguaje(request)
        return super(SignUp, self).post(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'refer' in self.request.GET:
            context['refer_id'] = self.request.GET.get('refer')
        return context

    def form_valid(self, form):        
        self.object = form.save(commit=False)
        if 'refer_id' in self.request.POST:
            self.object.refer_id = self.request.POST['refer_id']
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
