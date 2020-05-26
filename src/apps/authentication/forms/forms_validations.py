
import re

from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError


def white_spaces(value):
    """
    Valid white spaces in forms
    """
    if re.search(r'[\s]', value):
        raise ValidationError(_('El login no puede contener espacios en blanco'))


def positive_value(value):
    if value <= 0:
        raise ValidationError(_('el codigo debe ser un valor positivo.'))

def seven_characters(characters):
    if len(str(characters)) <= 6:
        raise ValidationError(_('el codigo debe tener 7 caracteres'))

    if len(str(characters)) >= 8:
        raise ValidationError(_('el codigo no puede contener mas de 7 caracteres'))

