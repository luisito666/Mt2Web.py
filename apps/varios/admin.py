# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

from django.contrib import admin
from apps.varios.models import Descarga, Top, RegistroCompras

# Register your models here.


class DescargaDisplay(admin.ModelAdmin):
    list_display = ('provedor', 'peso', 'fecha', 'link', 'publicado')
    search_fields = ['provedor']


class TopDisplay(admin.ModelAdmin):
    list_display = ('account_id', 'name', 'level', 'exp', 'ranking')
    search_fields = ['name']


class RegistroComprasDisplay(admin.ModelAdmin):
    list_display = ('ref_id', 'account_id', 'login', 'coins_compradas', 'status', 'fecha_compra')
    search_fields = ['login']


admin.site.register(Descarga, DescargaDisplay)
admin.site.register(Top, TopDisplay)
admin.site.register(RegistroCompras, RegistroComprasDisplay)
