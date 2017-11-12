from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

class Tag(models.Model):
	slug = models.SlugField(max_length=200, unique=True)

	def __str__(self):
		return self.slug


class EntradaQuerySet(models.QuerySet):
	def published(self):
		return self.filter(publicado=True)

class Entrada(models.Model):
	titulo = models.CharField(max_length=200)
	cuerpo = models.TextField()
	slug = models.SlugField(max_length=200, unique=True)
	publicado = models.BooleanField(default=True)
	creado = models.DateTimeField(auto_now_add=True)
	modificado = models.DateTimeField(auto_now=True)
	tags = models.ManyToManyField(Tag)

	objects = EntradaQuerySet.as_manager()

	def get_absolute_url(self):
		return reverse("blog:entry_detail", kwargs={"slug": self.slug })


	def __str__(self):
		return self.titulo

	class Meta:
		verbose_name = "Entrada del Blog"
		verbose_name_plural = "Entradas del blog"
		ordering = ["-creado"]
