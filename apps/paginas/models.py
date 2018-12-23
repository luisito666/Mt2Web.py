# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

from django.db import models
from django.core.urlresolvers import reverse

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

# Queryset personalizado
class PaginaQuerySet(models.QuerySet):
	def published(self):
		return self.filter(publicado=True)


class Pagina(models.Model):
    titulo = models.CharField(max_length=200)
    cuerpo = MarkdownxField()
    slug = models.SlugField(max_length=200, unique=True)
    publicado = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    objects = PaginaQuerySet.as_manager()

    @property
    def formatted_markdown(self):
        return markdownify(self.cuerpo)

    def get_absolute_url(self):
        return reverse("pages:page_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Pagina"
        verbose_name_plural = "Paginas"
        ordering = ["-creado"]

