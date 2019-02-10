# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# Django
from django.core.mail import send_mail

# Rest Framework 
from rest_framework import serializers

# Local models
from apps.account.models import Account


from apps.account.funciones import get_mail_register, aleatorio

# load settings
from core import settings

class RegisterSerializer(serializers.ModelSerializer):
    
    def validate(self, data):
        data['password'] = Account.password_hash(data['password'])
        return data
        
    def create(self, validated_data):
        cuenta = Account.objects.create(**validated_data)
        cuenta.address = aleatorio(40)
        cuenta.save()
        self.send_confirmation_email(cuenta.address)
        return {
			'login': validated_data['login'],
			'password': '***********',
			'real_name': validated_data['real_name'],
			'email': validated_data['email'],
			'social_id': validated_data['social_id']
		}

    def send_confirmation_email(self, key):
        try:
            send_mail(
                _('Bienvenido a ') + settings.SERVERNAME,
                settings.EMAIL_HOST_USER,
                [self.email],
                html_message=get_mail_register(self.login, key ),
            )
        except Exception as err:
            print(err)
    
    class Meta:
        model = Account
        fields = ('login', 'password', 'real_name', 'email', 'social_id')


