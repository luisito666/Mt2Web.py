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

# Importando el libería de encriptación
from hashlib import sha1

# Importando timezone
from datetime import datetime, timedelta


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
    refer_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'account'
        verbose_name = 'cuenta'
        verbose_name_plural = 'cuentas'

    def __str__(self):
        return self.login

    # Funcion para encryptar password
    @staticmethod
    def password_hash(password):
        """ generate a MySQL Password 
            is required for default in dbs of metin2
        """
        mysql_hash = '*'+sha1(sha1(password.encode()).digest()).hexdigest()  # Generando el hash
        mysql_hash = mysql_hash.upper()                                      # Convirtiendo el hash a mayusculas
        return mysql_hash                                                    # Retornando el hash

    def update_password(self, password):
        self.password = self.password_hash(password)

    def validate_password(self, password):
        validate = self.password_hash(password)
        return self.password == validate
    
    def is_active(self):
        """ Verifica que el usuario no este baneado.
        """
        if self.status == 'OK':
            return True
        return False
    
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

