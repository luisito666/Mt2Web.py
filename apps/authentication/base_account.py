from django.db import models
from django.utils.translation import gettext_lazy as _

# import hashers
from apps.authentication.hashers import make_password, validate_password, is_password_usable


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


