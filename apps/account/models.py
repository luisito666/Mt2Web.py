# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models

#model generado automaticamente por django.
#si no es compatible con tu base de datos generar uno nuevo
class Account(models.Model):
    login = models.CharField(unique=True, max_length=30)
    password = models.CharField(max_length=45)
    real_name = models.CharField(max_length=16, blank=True, null=True)
    social_id = models.CharField(max_length=13)
    email = models.CharField(max_length=64)
    phone1 = models.CharField(max_length=16, blank=True, null=True)
    phone2 = models.CharField(max_length=16, blank=True, null=True)
    address = models.CharField(max_length=128, blank=True, null=True)
    zipcode = models.CharField(max_length=7, blank=True, null=True)
    create_time = models.DateTimeField(default=timezone.now)
    question1 = models.CharField(max_length=48, blank=True, null=True)
    answer1 = models.CharField(max_length=48, blank=True, null=True)
    question2 = models.CharField(max_length=48, blank=True, null=True)
    answer2 = models.CharField(max_length=48, blank=True, null=True)
    is_testor = models.IntegerField(default=0)
    status = models.CharField(max_length=8,default="OK")
    securitycode = models.CharField(max_length=192, blank=True, null=True)
    newsletter = models.IntegerField(blank=True, null=True)
    empire = models.IntegerField(default=0)
    name_checked = models.IntegerField(default=0)
    availdt = models.DateTimeField(db_column='availDt',default="2020-01-01T00:00:00")  # Field name made lowercase.
    mileage = models.IntegerField(default=0)
    coins = models.IntegerField(default=0)
    gold_expire = models.DateTimeField(default="2020-01-01T00:00:00")
    silver_expire = models.DateTimeField(default="2020-01-01T00:00:00")
    safebox_expire = models.DateTimeField(default="2020-01-01T00:00:00")
    autoloot_expire = models.DateTimeField(default="2020-01-01T00:00:00")
    fish_mind_expire = models.DateTimeField(default="2020-01-01T00:00:00")
    marriage_fast_expire = models.DateTimeField(default="2020-01-01T00:00:00")
    money_drop_rate_expire = models.DateTimeField(default="2020-01-01T00:00:00")
    ttl_cash = models.IntegerField(default=0)
    ttl_mileage = models.IntegerField(default=0)
    channel_company = models.CharField(max_length=30)
    rang = models.IntegerField(blank=True, null=True)
    last_play = models.DateTimeField(default=timezone.now)
    lastvote = models.DateTimeField(default=timezone.now)
    day_of_vote = models.DateTimeField(default=timezone.now)
    cash = models.IntegerField(default=0)
    web_admin = models.IntegerField(default=0)
    web_ip = models.CharField(max_length=15,default=0)
    web_aktiviert = models.CharField(max_length=32)
    drs = models.IntegerField(default=0)
    reason = models.CharField(max_length=256, blank=True, null=True)
    web = models.IntegerField(default=0)
    marks = models.IntegerField(default=0)
    codigo_referido = models.CharField(max_length=32)
    referido = models.CharField(max_length=32)
    verificacion = models.CharField(db_column='Verificacion', max_length=32,default=0)  # Field name made lowercase.
    a_points = models.IntegerField(default=0)
    votecoins = models.IntegerField(default=0)
    token_expire = models.DateTimeField(blank=True, null=True)

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
