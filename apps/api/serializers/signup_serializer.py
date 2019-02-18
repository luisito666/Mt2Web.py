# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# Django
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

# Rest Framework 
from rest_framework import serializers

# Local models
from apps.account.models import Account


from apps.account.funciones import get_mail_register, aleatorio
from apps.api.state import User
from .token_serializer import PasswordField

# load settings
from core import settings


class SignupBaseSerializer(serializers.Serializer):
    username_field = User.USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super(SignupBaseSerializer, self).__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField()
        self.fields['email'] = serializers.EmailField()
        self.fields['real_name'] = serializers.CharField()
        self.fields['social_id'] = serializers.IntegerField()


    def validate(self, attrs):        
        self.user = User.objects.create_account(**{
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
            'email': attrs['email'],
            'real_name': attrs['real_name'],
            'social_id': attrs['social_id']
        })

        if self.user is None:
            raise serializers.ValidationError(
                _('Error in create user')
            )

        return {
            'username': self.user.login,
            'email': self.user.email,
            'real_name': self.user.real_name,
            'social_id': self.user.social_id
        }


class SigupSerializer(SignupBaseSerializer):
    
    def validate(self, attrs):
        data = super(SigupSerializer, self).validate(attrs)

        self.send_confirmation_email('mikey')

        return data


    def send_confirmation_email(self, key):
        try:
            send_mail(
                _('Bienvenido a ') + settings.SERVERNAME,
                settings.EMAIL_HOST_USER,
                [self.user.email],
                html_message=get_mail_register(self.user.login, key ),
            )
        except Exception as err:
            print(err)


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


