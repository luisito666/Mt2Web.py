
from . import forms_errors
from . import forms_validations

from django import forms
from django.utils.translation import ugettext_lazy as _

from ..models import Account

class AccountCreationForm(forms.ModelForm):
    login = forms.CharField(
        label=_('Nombre de usuario'),
        min_length=4,
        max_length=30,       
        error_messages=forms_errors.MESSAGES_USER,
        validators=[forms_validations.white_spaces]
    )
    password = forms.CharField(
        min_length=5,
        max_length=30,
        widget=forms.PasswordInput(),
        error_messages=forms_errors.MESSAGES_PASSWORD,
        validators=[forms_validations.white_spaces]
    )
    real_name = forms.CharField(
        label=_('Nombre real'),
        min_length=4,
        max_length=50,
        error_messages=forms_errors.MESSAGES_GENERAL
    )
    email = forms.EmailField(
        max_length=50,
        error_messages=forms_errors.MESSAGES_EMAIL
    )
    social_id = forms.IntegerField(
        label=_('Codigo de borrado'),
        error_messages=forms_errors.MESSAGES_GENERAL,
        validators=[forms_validations.seven_characters]
    )

    class Meta:
        model = Account
        fields = [
            'login',
            'password',
            'real_name',
            'email',
            'social_id',
        ]
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
    

