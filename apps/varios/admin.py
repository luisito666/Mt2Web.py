from django.contrib import admin
from apps.varios.models import Descarga, Top

# Register your models here.

class DescargaDisplay(admin.ModelAdmin):
	list_display = ('provedor','peso','fecha','link')
	search_fields = ['provedor']

class TopDisplay(admin.ModelAdmin):
	list_display = ('account_id','name','level','exp', 'ranking')
	search_fields = ['name']


admin.site.register(Descarga, DescargaDisplay )
admin.site.register(Top, TopDisplay)