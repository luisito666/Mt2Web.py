# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# Django Imports
from django.shortcuts import render
from django.views import View

# import modelos
from apps.varios.models import Descarga

# importando funciones
from apps.account.funciones import lenguaje


# Clase usada para la pagina de descargas.
class Downloads(View):
    model = Descarga
    template_name = 'account/download.html'

    def get(self, request):
        lenguaje(request)

        context = {
            'descarga': self.model.objects.publicado(),
        }
        return render(request, self.template_name, context)

