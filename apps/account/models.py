# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# Importaciones por default.
from __future__ import unicode_literals
from django.db import models

# Importando timezone
from django.utils import timezone

# Importando el archivo de configuracion
from core import settings

# Importando el libería de encriptación
from hashlib import sha1


# modelo generico compatible con todas las bases de datos
class Account(models.Model):
    STATUS_ACCOUNT = (
        ('OK', 'Disponible'),
        ('BLOCK', 'Baneado'),
    )
    login = models.CharField(unique=True, max_length=30)
    password = models.CharField(max_length=45)
    real_name = models.CharField(max_length=16, blank=True, null=True)
    social_id = models.CharField(max_length=13)
    email = models.CharField(max_length=64)
    address = models.CharField(max_length=128, blank=True, null=True)
    status = models.CharField(max_length=8,default="OK", choices=STATUS_ACCOUNT)
    coins = models.IntegerField(default=0)
    create_time = models.DateTimeField(default=timezone.now)
    availdt = models.DateTimeField(db_column='availDt',default=settings.ACTIVATE)
    gold_expire = models.DateTimeField(default=settings.BUFFSTUF)
    silver_expire = models.DateTimeField(default=settings.BUFFSTUF)
    safebox_expire = models.DateTimeField(default=settings.BUFFSTUF)
    autoloot_expire = models.DateTimeField(default=settings.BUFFSTUF)
    fish_mind_expire = models.DateTimeField(default=settings.BUFFSTUF)
    marriage_fast_expire = models.DateTimeField(default=settings.BUFFSTUF)
    money_drop_rate_expire = models.DateTimeField(default=settings.BUFFSTUF)
    token_expire = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'account'
        verbose_name = 'cuenta'
        verbose_name_plural = 'cuentas'

    def __str__(self):
        return self.login

    # Funcion para encryptar password
    @staticmethod
    def micryp(password):
        mysql_hash = '*'+sha1(sha1(password.encode()).digest()).hexdigest()  # Generando el hash
        mysql_hash = mysql_hash.upper()                                      # Convirtiendo el hash a mayusculas
        return mysql_hash                                                    # Retornando el hash
