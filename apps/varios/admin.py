from django.contrib import admin
from apps.varios.models import Descarga, Top, RegistroCompras

# Register your models here.

class DescargaDisplay(admin.ModelAdmin):
	list_display = ('provedor','peso','fecha','link')
	search_fields = ['provedor']

class TopDisplay(admin.ModelAdmin):
	list_display = ('account_id','name','level','exp', 'ranking')
	search_fields = ['name']

class RegistroComprasDisplay(admin.ModelAdmin):
	list_display = ('ref_id','account_id','login','coins_compradas','status')
	search_fields = ['login']

admin.site.register(Descarga, DescargaDisplay )
admin.site.register(Top, TopDisplay)
admin.site.register(RegistroCompras,RegistroComprasDisplay)
