# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# importaciones que se realizan por defecto
from django import forms
from django.core.mail import send_mail

# importando lo modelos que se usaran en los formularios
from apps.authentication.models import Account
from apps.authentication.hashers import make_password

# importando ugettext_lazy
from django.utils.translation import ugettext_lazy as _

# importando el capcha de los formularios
from captcha.fields import ReCaptchaField

from apps.account.funciones import aleatorio, get_mail_register

from core import settings
# impoortanfo re - es usado para validar el login
import re

# Diccionarios Espaciales con mensajes de error

ERROR_MESSAGES_USER = {
                        'required': _('el nombre de usuario es requerido'),
                        'unique': _('el nombre de usuario ya esta registrado'),
                        'invalid': _('ingrese un nombre de usuario valido'),
                      }

ERROR_MESSAGES_GENERAL = {
                        'required': _('este campo es requerido'),
                      }

ERROR_MESSAGES_PASSWORD = {
                          'required': _('el password es requerido')
                          }

ERROR_MESSAGES_EMAIL = {
                          'required': _('el email es requerido'),
                          'invalid': _('ingrese un correo valido'),
                        }


# Funciones que realizan validaciones en los formularios


# validando espacios en blanco
def valida_5(value_login):
    if re.search(r'[\s]', value_login):
        raise forms.ValidationError(_('El login no puede contener espacios en blanco'))


# validando caracteres login
def valida_6(value_login):
    if len(value_login) <= 4:
        raise forms.ValidationError(_('el nombre de usuario debe contener mas de 4 caracteres'))


# validando caracteres de password
def must_be_gt(value_password):
    if len(value_password) < 5:
        raise forms.ValidationError(_('el password debe contener por lo menos 5 caracteres'))


# validando que el sociial id sea positivo
def valida_2(value_social_id):
    if value_social_id <= 0:
        raise forms.ValidationError(_('el codigo debe ser un valor positivo.'))


# validando que el social id tenga sea mayor o igual 6
def valida_3(value_social_id):
    if len(str(value_social_id)) <= 6:
        raise forms.ValidationError(_('el codigo debe tener 7 caracteres'))


# validando que el social id tenga menos de 8 caracteres
def valida_4(value_social_id):
    if len(str(value_social_id)) >= 8:
        raise forms.ValidationError(_('el codigo no puede contener mas de 7 caracteres'))


# validando formulario desbug personajes
def valida_7(value_login):
    if re.search(r'[\s]', value_login):
        raise forms.ValidationError(_('El campo no puede contener espacios en blanco'))


""" Este formulario por la herencia que tiene form.ModelForm si necesita un modelo para su funcionamiento
de lo contrario no funcionara """


# Formulario de registro principal
class CreateUserForm(forms.ModelForm):
    login = forms.CharField(label=_('Nombre de Usuario'),
                            max_length=30,
                            error_messages=ERROR_MESSAGES_USER,
                            validators=[valida_5, valida_6])
    password = forms.CharField(max_length=30,
                               widget=forms.PasswordInput(),
                               validators=[must_be_gt],
                               error_messages=ERROR_MESSAGES_PASSWORD)
    real_name = forms.CharField(label=_('Nombre real'),
                                max_length=50,
                                error_messages=ERROR_MESSAGES_GENERAL)
    email = forms.EmailField(max_length=30,
                             error_messages=ERROR_MESSAGES_EMAIL)
    social_id = forms.IntegerField(label=_('Codigo de borrado'),
                                   error_messages=ERROR_MESSAGES_GENERAL,
                                   validators=[valida_2, valida_3, valida_4])
    if settings.RECAPTCHA:
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

    def clean_password(self):
        password = self.cleaned_data['password']
        data = make_password(password)
        return data
    
    def create(self, data):
        instance = super(CreateUserForm, self).save(commit=False)    
        # generando key de email        
        instance.address = aleatorio(40)
        instance.save()
        self.send_confirmation_email(instance.address)

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


"""Los siguiente formularios heredan de la clase forms.Form por lo que no necesitan
de un modelo para su funcionamiento  """


# Este formulario se usa para el login
class CustomLoginForm(forms.Form):
    login = forms.CharField(label=_('Usuario'), max_length=30, validators=[valida_5])
    password = forms.CharField(max_length=30,
                               widget=forms.PasswordInput(),
                               validators=[must_be_gt],
                               error_messages=ERROR_MESSAGES_PASSWORD)

    if settings.RECAPTCHA:
        capcha = ReCaptchaField()


# Este formulario es para desbuguear player
class CustomDesbugForm(forms.Form):
    nombre = forms.CharField(max_length=30, validators=[valida_7])


# Este es el formulario que usaremos para el cambio de password
class CustomChangePassword(forms.Form):
    password = forms.CharField(max_length=30,
                               widget=forms.PasswordInput(),
                               validators=[must_be_gt],
                               error_messages=ERROR_MESSAGES_PASSWORD)
    new_password = forms.CharField(max_length=30,
                                   widget=forms.PasswordInput(),
                                   validators=[must_be_gt],
                                   error_messages=ERROR_MESSAGES_PASSWORD)
    new_password_again = forms.CharField(max_length=30,
                                         widget=forms.PasswordInput(),
                                         validators=[must_be_gt],
                                         error_messages=ERROR_MESSAGES_PASSWORD)


# Este formulario se usa para recuperar password por correo
class ResPassword(forms.Form):
    login = forms.CharField(label=_('Usuario'), max_length=30, validators=[valida_5])
    email = forms.CharField(max_length=30, validators=[valida_5], error_messages=ERROR_MESSAGES_PASSWORD)

    if settings.RECAPTCHA:
        capcha = ReCaptchaField()


class FormResetPassword(forms.Form):
    password = forms.CharField(max_length=30,
                               widget=forms.PasswordInput(),
                               validators=[must_be_gt],
                               error_messages=ERROR_MESSAGES_PASSWORD)
    password_again = forms.CharField(max_length=30,
                                     widget=forms.PasswordInput(),
                                     validators=[must_be_gt],
                                     error_messages=ERROR_MESSAGES_PASSWORD)


class FormRequestPassword(forms.Form):
    email = forms.EmailField(max_length=30,
                             error_messages=ERROR_MESSAGES_EMAIL)
    if settings.RECAPTCHA:
        capcha = ReCaptchaField()
