from django.contrib import admin
from django.db import models
from markdownx.admin import MarkdownxModelAdmin
from markdownx.widgets import AdminMarkdownxWidget
# Register your models here.
from .models import Pagina

class PaginaAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget }
    }

admin.site.register(Pagina, MarkdownxModelAdmin)