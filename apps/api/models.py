
from django.utils.functional import cached_property
from .settings import api_settings

class TokenUser(object):

    username = ''

    is_active = True

    def __init__(self, token):
        self.token = token
    
    def __str__(self):
        return 'TokenUser {}'.format(self.id)

    @cached_property
    def id(self):
        return self.token[api_settings.USER_ID_CLAIM]

    @cached_property
    def pk(self):
        return self.id
    
    def save(self):
        raise NotImplementedError('Token users have no DB representation')

    def delete(self):
        raise NotImplementedError('Token users have no DB representation')

    def set_password(self, raw_password):
        raise NotImplementedError('Token users have no DB representation')

    def check_password(self, raw_password):
        raise NotImplementedError('Token users have no DB representation')
    
    def has_perm(self, perm, obj=None):
        return False
    
    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True
    
