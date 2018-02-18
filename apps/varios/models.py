# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

from django.db import models
from django.utils import timezone

# Create your models here.

class DescargaQuerySet(models.QuerySet):
	def publicado(self):
		return self.filter(publicado=True)

class Descarga(models.Model):
	provedor = models.CharField(max_length=30)
	peso = models.DecimalField(max_digits=5, decimal_places=3)
	fecha = models.DateTimeField(default=timezone.now)
	link = models.CharField(max_length=100)
	publicado = models.BooleanField(default=True)

	objects = DescargaQuerySet.as_manager()

	def __str__(self):
		return self.link

	class Meta:
		verbose_name = 'Descarga'
		verbose_name_plural = 'Descargas'


class Top(models.Model):
    account_id = models.IntegerField()
    name = models.CharField(max_length=26)
    guild_name = models.CharField(max_length=26, null=True)
    level = models.IntegerField()
    exp = models.IntegerField()
    ranking = models.SmallIntegerField(blank=True, null=True)

    def __str__(self):
    	return self.name

	class Meta:
		verbose_name = 'Personaje'
		verbose_name_plural = 'Personajes'

class RegistroCompras(models.Model):
	ref_id = models.IntegerField()
	account_id = models.IntegerField()
	login = models.CharField(max_length=30)
	coins_compradas = models.IntegerField()
	status = models.BooleanField(default=False)
	fecha_compra = models.DateTimeField()

	def __str__(self):
		return self.login

	class Meta:
		verbose_name = 'Registro Compra'
		verbose_name_plural = 'Registro Compras'
