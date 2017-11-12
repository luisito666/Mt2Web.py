from django.contrib import admin

# Register your models here.
#importando modelos a visualar en interface administrativa
from apps.account import models

#creando el modelo a registar
class AccountDisplay(admin.ModelAdmin):
	list_display = ('id', 'login', 'real_name', 'email', 'status', 'coins', 'a_points', 'votecoins')
	search_fields = ['login' , 'real_name']


#Registrando modelos en interface administrativa
admin.site.register(models.Account, AccountDisplay)