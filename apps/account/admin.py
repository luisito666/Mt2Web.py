# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php
from django.contrib import admin

#importando modelos a visualar en interface administrativa
from apps.account import models


# creando el modelo a registar
class AccountDisplay(admin.ModelAdmin):
    list_display = ('id', 'login', 'real_name', 'email', 'status', 'availdt')
    search_fields = ['refer_id', 'login', 'email']


# Registrando modelos en interface administrativa
admin.site.register(models.Account, AccountDisplay)
