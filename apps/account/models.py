# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

from __future__ import unicode_literals
from django.utils import timezone
from django.db import models

#modelo generico compatible con todas las bases de datos
class Account(models.Model):
    login = models.CharField(unique=True, max_length=30)
    password = models.CharField(max_length=45)
    real_name = models.CharField(max_length=16, blank=True, null=True)
    social_id = models.CharField(max_length=13)
    email = models.CharField(max_length=64)
    address = models.CharField(max_length=128, blank=True, null=True)
    coins = models.IntegerField(default=0)
    create_time = models.DateTimeField(default=timezone.now)
    availdt = models.DateTimeField(db_column='availDt',default="2020-01-01T00:00:00")
    #token_expire = models.DateTimeField(blank=True, null=True) #Descomentar cuando se crea el campo en la bd

    class Meta:
        db_table = 'account'
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'

    def __str__(self):
        return self.login

    #Funcion para encryptar password
    def micryp(password,other):
        from django.db import connection, transaction
        cursor = connection.cursor()
        #cursor.execute("select PASSWORD(%s)",other)
        cursor.execute("select PASSWORD('%s')" % other)
        row = cursor.fetchone()
        cursor.close()
        start = str(row)
        valor = start.count(start)
        control = 0
        s = ""
        for letra in row:
            if control > 3 or control < 49:
                s += letra
        control = control + 1
        return s
