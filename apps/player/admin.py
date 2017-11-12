from django.contrib import admin

from apps.player import models

class PlayerDisplay(admin.ModelAdmin):
	list_display = ('name', 'master', 'level','exp','gold', 'win')
	search_fields = ['name']


#admin.site.register(models.Guild, PlayerDisplay)