
# from django
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

# from rest framework
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions

# local models
from apps.account.models import Account

class TokenAuthentication(BaseAuthentication):
    """ Clients should authenticate by passing the token key in the "Authorization"
        HTTP header, prepended with the string "Token ".  For example:

        this implementation use Account model insteance of django users

        Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'Bearer'
    
    def authenticate(self, request):
        auth_type, token = get_authorization_header(request).split(' ')
        if auth_type == self.keyword:
            raise exceptions.AuthenticationFailed(_('Only Acept Bearer Tokens'))
        # validate token
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        user = Account.verify_auth_token(token)
        if user is None:
            raise exceptions.AuthenticationFailed(_('Invalid User validation'))
        return ( user )
    
    def authenticate_header(self, request):
        return self.keyword

