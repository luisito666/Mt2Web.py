from django.db import models
from django.utils import timezone

# Create your models here.

class Descarga(models.Model):
	provedor = models.CharField(max_length=30)
	peso = models.DecimalField(max_digits=5, decimal_places=3)
	fecha = models.DateTimeField(default=timezone.now)
	link = models.CharField(max_length=100)

	def __str__(self):
		return self.provedor

class Top(models.Model):
    account_id = models.IntegerField()
    name = models.CharField(max_length=26)
    guild_name = models.CharField(max_length=26, null=True)
    level = models.IntegerField()
    exp = models.IntegerField()
    ranking = models.SmallIntegerField(blank=True, null=True)


    def __str__(self):
    	return self.name

class RegistroCompras(models.Model):
	ref_id = models.IntegerField()
	account_id = models.IntegerField()
	login = models.CharField(max_length=30)
	coins_compradas = models.IntegerField()
	status = models.BooleanField(default=False)

	def __str__(self):
		return self.login
