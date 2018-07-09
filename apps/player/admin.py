# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

from django.contrib import admin

from apps.player import models


class PlayerDisplay(admin.ModelAdmin):
    list_display = ('name', 'master', 'level', 'exp', 'gold', 'win')
    search_fields = ['name']

# admin.site.register(models.Guild, PlayerDisplay)
