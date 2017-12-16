#importaciones que se realizan por defecto
from django import forms

#importando lo modelos que se usaran en los formularios
from django.contrib.auth.models import User
from apps.account.models import Account

#importando los modelos de django
from django.db import models

#importando datetime
from datetime import datetime

#importando funcion daa
from django.utils.translation import ugettext_lazy as _

#importando el capcha de los formularios
from captcha.fields import ReCaptchaField

import re

"""
Diccionarios Espaciales con mensajes de error
"""
ERROR_MESSAGES_USER = {
                        'required': 'el nombre de usuario es requerido',
                        'unique': 'el nombre de usuario ya esta registrado',
                        'invalid': 'ingrese un nombre de usuario valido',
                      }

ERROR_MESSAGES_GENERAL = {
                        'required': 'este campo es requerido',
                      }

ERROR_MESSAGES_PASSWORD = {
                          'required': 'el password es requerido'
                          }

ERROR_MESSAGES_EMAIL =  {
                          'required': 'el email es requerido',
                          'invalid': 'ingrese un correo valido',
                        }

"""
Funciones que realizan validaciones en los formularios
"""

def valida_5(value_login):
  if re.search(r'[\s]', value_login):
    raise forms.ValidationError('El login no puede contener espacios en blanco')

def valida_6(value_login):
  if len(value_login) <= 4:
    raise forms.ValidationError('el nombre de usuario debe contener mas de 4 caracteres')

def must_be_gt(value_password):
  if len(value_password) < 5:
    raise forms.ValidationError('el password debe contener por lo menos 5 caracteres')

def valida_2(value_social_id):
  if value_social_id <= 0:
    raise forms.ValidationError('el codigo debe ser un valor positivo.')

def valida_3(value_social_id):
  if len(str(value_social_id)) <= 6:
    raise forms.ValidationError('el codigo debe tener 7 caracteres')

def valida_4(value_social_id):
  if len(str(value_social_id)) >= 8:
    raise forms.ValidationError('el codigo no puede contener mas de 7 caracteres')

def valida_7(value_login):
  if re.search(r'[\s]', value_login):
    raise forms.ValidationError('El campo no puede contener espacios en blanco')

""" Este formulario por la herencia que tiene form.ModelForm si necesita un modelo para su funcionamiento
de lo contrario no funcionara """

#Formulario de registro principal
class CreateUserForm(forms.ModelForm):
  login = forms.CharField(label='Nombre de Usuario',max_length=30, error_messages = ERROR_MESSAGES_USER, validators = [valida_5, valida_6])
  password = forms.CharField(max_length=30, widget = forms.PasswordInput(), validators = [must_be_gt] ,error_messages = ERROR_MESSAGES_PASSWORD)
  real_name = forms.CharField(label='Nombre real',max_length=50, error_messages = ERROR_MESSAGES_GENERAL)
  email = forms.EmailField(max_length=30 , error_messages = ERROR_MESSAGES_EMAIL )
  social_id = forms.IntegerField(label='Codigo de borrado' ,error_messages = ERROR_MESSAGES_GENERAL, validators = [valida_2, valida_3, valida_4])
  capcha = ReCaptchaField()

  class Meta:
    model = Account
    fields = [
      'login',
      'password',
      'real_name',
      'email',
      'social_id',
    ]


"""Los siguiente formularios heredan de la clase forms.Form por lo que no necesitan
de un modelo para su funcionamiento  """

#Este formulario se usa para el login
class CustomLoginForm(forms.Form):
  login = forms.CharField(label='Usuario',max_length=30, validators=[valida_5])
  password = forms.CharField(max_length=30, widget = forms.PasswordInput(), validators = [must_be_gt] ,error_messages = ERROR_MESSAGES_PASSWORD)
  capcha = ReCaptchaField()

#Este formulario es para desbuguear player
class CustomDesbugForm(forms.Form):
  nombre = forms.CharField(max_length=30, validators=[valida_7])

#Este es el formulario que usaremos para el cambio de password
class CustomChangePassword(forms.Form):
  password = forms.CharField(max_length=30, widget = forms.PasswordInput(), validators = [must_be_gt] ,error_messages = ERROR_MESSAGES_PASSWORD)
  new_password = forms.CharField(max_length=30, widget = forms.PasswordInput(), validators = [must_be_gt] ,error_messages = ERROR_MESSAGES_PASSWORD)
  new_password_again = forms.CharField(max_length=30, widget = forms.PasswordInput(), validators = [must_be_gt] ,error_messages = ERROR_MESSAGES_PASSWORD)

#Este formulario se usa para recuperar password por correo
class ResPassword(forms.Form):
  login = forms.CharField(label='Usuario',max_length=30, validators=[valida_5])
  email = forms.CharField(max_length=30, validators = [valida_5] ,error_messages = ERROR_MESSAGES_PASSWORD)
  capcha = ReCaptchaField()

class FormResetPassword(forms.Form):
  password = forms.CharField(max_length=30, widget = forms.PasswordInput(), validators = [must_be_gt] ,error_messages = ERROR_MESSAGES_PASSWORD)
  password_again = forms.CharField(max_length=30, widget = forms.PasswordInput(), validators = [must_be_gt] ,error_messages = ERROR_MESSAGES_PASSWORD)
