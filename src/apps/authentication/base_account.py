from django.db import models
from django.utils.translation import gettext_lazy as _

from django.utils.crypto import get_random_string, salted_hmac  

# import hashers
from apps.authentication.hashers import make_password, validate_password, is_password_usable


class BaseAccountManager(models.Manager):
    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = email_name + '@' + domain_part.lower()
        return email
    
    def make_random_password(self, length=10,
                             allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                           'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                            '23456789'):
        return get_random_string(length, allowed_chars)
    
    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class AbstractBaseAccount(models.Model):
    STATUS_ACCOUNT = (
        ('OK', 'Disponible'),
        ('BLOCK', 'Baneado'),
    )
    password = models.CharField(_('password'), max_length=45)
    status = models.CharField(max_length=8,default="OK", choices=STATUS_ACCOUNT)

    class Meta:
        abstract = True

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True
    
    @property
    def is_banned(self):
        if self.status == 'BLOCK':
            return True
        return False
        
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password
    
    def check_password(self, raw_password):
        return validate_password(self.password, raw_password)
    
    def set_unusable_password(self):
        self.password = make_password(None)
    
    def has_usable_password(self):
        return is_password_usable(self.password)

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        key_salt = "apps.authentication.base_account.AbstractBaseAccount.get_session_auth_hash"
        return salted_hmac(key_salt, self.password).hexdigest()


