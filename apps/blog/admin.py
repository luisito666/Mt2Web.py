from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from django_markdown.widgets import AdminMarkdownWidget
from django.db.models import TextField

from apps.blog import models
# Register your models 

class EntradaAdmin(MarkdownModelAdmin):
	list_display = ("titulo", "creado")
	prepopulated_fields = {"slug": ("titulo",)}
	formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}


admin.site.register(models.Entrada, EntradaAdmin)
admin.site.register(models.Tag)