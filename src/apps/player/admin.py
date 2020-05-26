# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

from django.contrib import admin

from apps.varios.models import Top


class PlayerDisplay(admin.ModelAdmin):
    list_display = ('account_id', 'name', 'level', 'exp', 'ranking', 'ip')
    search_fields = ['name', 'account_id', 'ip']


# admin.site.register(Top, PlayerDisplay)
