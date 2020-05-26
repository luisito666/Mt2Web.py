from uuid import uuid4

from django.utils.translation import ugettext_lazy as _
from django.utils.six import text_type


from .exceptions import TokenError, TokenBackendError


from apps.api.settings import api_settings
from apps.api.utils import (
    aware_utcnow, datetime_from_epoch, datetime_to_epoch, format_lazy
)


class Token(object):
    """
    """
    token_type = None
    lifetime = None

    def __init__(self, token=None, verify=True):
        """
        """
        if self.token_type is None or self.lifetime is None:
            raise TokenError(_('Cannot create token with no type or lifetime'))
        
        self.token = token
        self.current_time = aware_utcnow()

        # Configurar el token
        if token is not None:
            # un token codificado ha sido provisionado
            from .state import token_backend

            # decodificando el token
            try:
                self.payload = token_backend.decode(token, verify=verify)
            except TokenBackendError:
                raise TokenBackendError(_('Token is invalid or expired'))
            
            if verify:
                self.verify()
        else:
            # new Token
            self.payload = {api_settings.TOKEN_TYPE_CLAIM: self.token_type}

            # set exp
            self.set_exp(from_time=self.current_time, lifetime=self.lifetime)

            # Set "jti" claim
            self.set_jti()

    def __repr__(self):
        return repr(self.payload)

    def __getitem__(self, key):
        return self.payload[key]

    def __setitem__(self, key, value):
        self.payload[key] = value

    def __delitem__(self, key):
        del self.payload[key]

    def __contains__(self, key):
        return key in self.payload

    def get(self, key, default=None):
        return self.payload.get(key, default)
    
    def __str__(self):
        """
        Signs and returns a token as a base64 encoded string.
        """
        from .state import token_backend

        return token_backend.encode(self.payload)

    def verify(self):
        self.check_exp()

        # Ensure token id is present
        if 'jti' not in self.payload:
            raise TokenError(_('Token has no id'))

        self.verify_token_type()
    
    def verify_token_type(self):
        """
        Ensures that the token type claim is present and has the correct value.
        """
        try:
            token_type = self.payload[api_settings.TOKEN_TYPE_CLAIM]
        except KeyError:
            raise TokenError(_('Token has no type'))

        if self.token_type != token_type:
            raise TokenError(_('Token has wrong type'))
    
    def set_jti(self):
        """
        Populates the "jti" claim of a token with a string where there is a
        negligible probability that the same string will be chosen at a
        later time.
        See here:
        https://tools.ietf.org/html/rfc7519#section-4.1.7
        """
        self.payload['jti'] = uuid4().hex
    
    def set_exp(self, claim='exp', from_time=None, lifetime=None):
        """
        Updates the expiration time of a token.
        """
        if from_time is None:
            from_time = self.current_time
        
        if lifetime is None:
            lifetime = self.lifetime
        
        self.payload[claim] = datetime_to_epoch(from_time + lifetime)

    def check_exp(self, claim='exp', current_time=None):
        """
        Checks whether a timestamp value in the given claim has passed (since
        the given datetime value in `current_time`).  Raises a TokenError with
        a user-facing error message if so.
        """
        if current_time is None:
            current_time = self.current_time
        
        try:
            claim_value = self.payload[claim]
        except KeyError:
            raise TokenError(format_lazy(_("Token has no '{}' claim"), claim))
        
        claim_time = datetime_from_epoch(claim_value)
        if claim_time <= current_time:
            raise TokenError(format_lazy(_("Token '{}' claim has expired"), claim))

    @classmethod
    def for_user(cls, user):
        """
        Returns an authorization token for the given user that will be provided
        after authenticating the user's credentials.
        """
        user_id = getattr(user, api_settings.USER_ID_FIELD)
        if not isinstance(user_id, int):
            user_id = text_type(user_id)
        
        token = cls()
        token[api_settings.USER_ID_CLAIM] = user_id

        return token


class AccessToken(Token):
    token_type = 'access'
    lifetime = api_settings.ACCESS_TOKEN_LIFETIME

