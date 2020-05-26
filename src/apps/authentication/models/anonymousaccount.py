""" AnonimousUser implementation """

ERROR_MESSAGES = {
    'general': 'No existe en la base de datos una representacion de un usuario anonimo'
}

class AnonymousAccount:
    id = None
    pk = None
    login = ''

    def __str__(self):
        return 'AnonymousAccount'
    
    @property
    def is_authenticated(self):
        return False
    
    @property
    def is_banned(self):
        return True
    
    def delete(self):
        raise NotImplementedError(ERROR_MESSAGES['general'])
    
    def save(self):
        raise NotImplementedError(ERROR_MESSAGES['general'])
    
    def set_password(self):
        raise NotImplementedError(ERROR_MESSAGES['general'])
    
    def check_password(self):
        raise NotImplementedError(ERROR_MESSAGES['general'])
    
    def set_unusable_password(self):
        raise NotImplementedError(ERROR_MESSAGES['general'])
    
    def has_usable_password(self):
        raise NotImplementedError(ERROR_MESSAGES['general'])
    
        
    
