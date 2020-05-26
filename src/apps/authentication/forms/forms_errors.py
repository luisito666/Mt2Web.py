from django.utils.translation import ugettext_lazy as _


MESSAGES_USER = {
    'required': _('el nombre de usuario es requerido'),
    'unique': _('el nombre de usuario ya esta registrado'),
    'invalid': _('ingrese un nombre de usuario valido'),
}

MESSAGES_GENERAL = {
    'required': _('este campo es requerido'),
}

MESSAGES_PASSWORD = {
    'required': _('el password es requerido')
}

MESSAGES_EMAIL = {
    'required': _('el email es requerido'),
    'invalid': _('ingrese un correo valido'),
}
