from __future__ import unicode_literals

# Django
from django.utils.translation import gettext_lazy as _
from django.utils.six import text_type

# Django rest framework
from rest_framework import serializers

# apps
from apps.api.state import User
from apps.api.tokens import AccessToken
from apps.authentication import authenticate


class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('style', {})

        kwargs['style']['input_type'] = 'password'
        kwargs['write_only'] = True

        return super(PasswordField, self).__init__(*args, **kwargs)


class TokenObtainBaseSerializer(serializers.Serializer):
    username_field = User.USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super(TokenObtainBaseSerializer, self).__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField()
    
    def validate(self, attrs):
        self.user = authenticate(**{
            self.username_field: attrs[self.username_field],
            'password': attrs['password']
        })

        if self.user is None or self.user.is_banned:
            raise serializers.ValidationError(
                _('No active account found with the given credentials')
            )
        
        return {}
    
    @classmethod
    def get_token(cls, user):
        raise NotImplemented('Must implement `get_token` method for `TokenObtainSerializer` subclasses')


class TokenObtainSerializer(TokenObtainBaseSerializer):
    @classmethod
    def get_token(cls, user):
        return AccessToken.for_user(user)
    
    def validate(self, attrs):
        # data = super(TokenObtainSerializer, self).validate(attrs)
        data = super(TokenObtainSerializer, self).validate(attrs)
        token = self.get_token(self.user)

        # data['token'] = text_type(token)
        data['login'] = text_type(token)

        return data
