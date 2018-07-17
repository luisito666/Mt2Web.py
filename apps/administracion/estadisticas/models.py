# Copyright (c) 2017-2018 ferchoafta@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

from django.db import models
from django.utils import timezone

# Create your models here.


class registroConectados(models.Model):
	time = models.DateTimeField()
	count = models.IntegerField()
	 

	def __str__(self):
		return "Fecha"

	class Meta:
		verbose_name = 'registro de conexión'
		verbose_name_plural = 'registro de conexiones'
