# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# libs
import jwt

# rest framework
from rest_framework import exceptions

# Importaciones por default.
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Importando el archivo de configuracion
from core import settings

# Importando timezone
from datetime import datetime, timedelta

from apps.authentication.base_account import AbstractBaseAccount


class NewAbstractAccount(AbstractBaseAccount):
    login = models.CharField(unique=True, max_length=30)
    real_name = models.CharField(max_length=16, null=True)
    social_id = models.CharField(max_length=13)
    email = models.CharField(max_length=64)
    address = models.CharField(max_length=128, null=True)
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
    token_expire = models.DateTimeField(null=True)
    refer_id = models.IntegerField(null=True)
    last_play = models.DateTimeField(default=settings.BUFFSTUF)
    ticket_id = models.CharField(max_length=30, default='')
    web_ip = models.CharField(max_length=15, default='0.0.0.0')
    web_aktiviert = models.CharField(max_length=32, default='0')
    user_admin = models.CharField(max_length=15, default='')
    donation = models.FloatField(default=1)
    kwix_chm = models.CharField(max_length=255, default='')
    kwix_chm_code = models.CharField(max_length=255, default='')
    last_ip = models.CharField(max_length=255, default='0.0.0.0')
    register_ip = models.CharField(max_length=256, default='0.0.0.0')
    user_level = models.SmallIntegerField(default=1)
    ban_reason = models.CharField(max_length=256, default='')
    referrer_link = models.CharField(max_length=256, default='')
    referrer = models.CharField(max_length=256, default='')
    rb_points = models.IntegerField(default=1)
    ysifre = models.CharField(max_length=255, default='')
    yemail = models.CharField(max_length=255, default='')
    ylogin = models.CharField(max_length=255, default='')
    tkod = models.CharField(max_length=10, default='')
    ypass = models.CharField(max_length=255, default='')
    ban_neden = models.CharField(max_length=255, default='')
    durum = models.IntegerField(default=1)
    davet = models.IntegerField(default=1)
    davet_durum = models.IntegerField(default=1)
    ip = models.CharField(max_length=40, default='')
    tel_degisim = models.CharField(max_length=255)
    tel_sure = models.CharField(max_length=255, default='')
    mail_degisim = models.CharField(max_length=255, default='')
    email_kod = models.CharField(max_length=255, default='')
    email_onay = models.CharField(max_length=855, default='')
    ban_sure = models.CharField(max_length=855, default='')
    ban_time = models.CharField(max_length=855, default='')
    kim_banlamis = models.CharField(max_length=855, default='')
    token_expire = models.DateTimeField(null=True)

    class Meta:
        db_table = 'account'
        verbose_name = 'cuenta'
        verbose_name_plural = 'cuentas'
        abstract = True

    def __str__(self):
        return self.login

    @staticmethod
    def generate_auth_token(self):
        """
        :param user:
        :return: Token JWT
        """
        payload = {
            "sub": str(self.id),
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(days=1),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token
    
    @staticmethod
    def verify_auth_token(token):
        try:
            validate_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = Account.objects.get(id=validate_token['sub'])
            return user
        except jwt.PyJWTError:
            raise exceptions.AuthenticationFailed(_('Invalid Token error'))
        except Account.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid User validation'))
        return None


# modelo generico compatible con todas las bases de datos
class AbstractAccount(AbstractBaseAccount):
    login = models.CharField(unique=True, max_length=30)
    real_name = models.CharField(max_length=16, blank=True, null=True)
    social_id = models.CharField(max_length=13)
    email = models.CharField(max_length=64)
    address = models.CharField(max_length=128, blank=True, null=True)
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
    refer_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'account'
        verbose_name = 'cuenta'
        verbose_name_plural = 'cuentas'
        abstract = True

    def __str__(self):
        return self.login

    
    @staticmethod
    def generate_auth_token(self):
        """
        :param user:
        :return: Token JWT
        """
        payload = {
            "sub": str(self.id),
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(days=1),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token
    
    @staticmethod
    def verify_auth_token(token):
        try:
            validate_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = Account.objects.get(id=validate_token['sub'])
            return user
        except jwt.PyJWTError:
            raise exceptions.AuthenticationFailed(_('Invalid Token error'))
        except Account.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid User validation'))
        return None


class Account(NewAbstractAccount):
    pass
