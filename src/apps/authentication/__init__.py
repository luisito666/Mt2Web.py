import inspect
import re

from django.apps import apps as django_apps
from django.utils.module_loading import import_string 
from django.core.exceptions import ImproperlyConfigured
from django.utils.crypto import constant_time_compare
from django.middleware.csrf import rotate_token

from core import settings

from .signals import user_logged_in, user_logged_out, user_login_failed


SESSION_KEY = '_auth_account_id'
BACKEND_SESSION_KEY = '_auth_account_backend'
HASH_SESSION_KEY = '_auth_account_hash'

def load_backend(path):
    return import_string(path)()

def _get_backends(return_tuples=False):
    backends = []
    for backend_path in settings.CUSTOM_AUTHENTICATION_BACKENDS:
        backend = load_backend(backend_path)
        backends.append((backend, backend_path) if return_tuples else backend)
    if not backends:
        raise ImproperlyConfigured(
            'No authentication backends have been defined. Does '
            'CUSTOM_AUTHENTICATION_BACKENDS contain anything?'
        )
    return backends


def get_backend():
    return _get_backends(return_tuples=False)


def _clean_credentials(credentials):
    """
    Clean a dictionary of credentials of potentially sensitive info before
    sending to less secure functions.
    Not comprehensive - intended for user_login_failed signal
    """
    SENSITIVE_CREDENTIALS = re.compile('api|token|key|secret|password|signature', re.I)
    CLEANSED_SUBSTITUTE = '********************'
    for key in credentials:
        if SENSITIVE_CREDENTIALS.search(key):
            credentials[key] = CLEANSED_SUBSTITUTE
    return credentials

def _get_user_session_key(request):
    # This value in the session is always serialized to a string, so we need
    # to convert it back to Python whenever we access it.
    return get_user_model()._meta.pk.to_python(request.session[SESSION_KEY])


def get_user_model():
    try:
        return django_apps.get_model(settings.CUSTOM_AUTH_USER_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured("CUSTOM_AUTH_USER_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL refers to model '%s' that has not been installed" % settings.CUSTOM_AUTH_USER_MODEL
        )


def get_user(request):
    """
    """
    from .models import AnonymousAccount
    user = None

    try:
        # cuenta = get_user_model().objects.get(id=request.session[BACKEND_SESSION_KEY])
        user_id = _get_user_session_key(request)
        backend_path = request.session[BACKEND_SESSION_KEY]
    except KeyError:
        pass
    else:
        if backend_path in settings.CUSTOM_AUTHENTICATION_BACKENDS:
            backend = load_backend(backend_path)
            user = backend.get_user(user_id)
            # verify the session
            if hasattr(user, 'get_session_auth_hash'):
                session_hash = request.session.get(HASH_SESSION_KEY)
                session_hash_verified = session_hash and constant_time_compare(
                    session_hash,
                    user.get_session_auth_hash()
                )
                if not session_hash_verified:
                    request.session.flush()
                    user = None
    
    return user or AnonymousAccount()


def authenticate(request=None, **credentials):
    """
    """
    for backend, backend_path in _get_backends(return_tuples=True):
        try:
            inspect.getcallargs(backend.authenticate, request, **credentials)
        except TypeError:
            continue
        try:
            user = backend.authenticate(request, **credentials)
        except Exception:
            break
        if user is None:
            continue
        
        user.backend = backend_path
        return user
    # The credentials supplied are invalid to all backends, fire signal
    user_login_failed.send(sender=__name__, credentials=_clean_credentials(credentials), request=request)


def login(request, account, backend=None):
    session_auth_hash = ''
    if account is None:
        account = request.account

    if hasattr(account, 'get_session_auth_hash'):
        session_auth_hash = account.get_session_auth_hash()

    if SESSION_KEY in request.session:
        if _get_user_session_key(request) != account.pk or (
            session_auth_hash and
            not constant_time_compare(request.session.get(HASH_SESSION_KEY, ''), session_auth_hash)):
            # To avoid reusing another user's session, create a new, empty
            # session if the existing session corresponds to a different
            # authenticated user.
            request.session.flush()
    else:
        request.session.cycle_key()
    try:
        backend = backend or account.backend
    except AttributeError:
        backends = _get_backends(return_tuples=True)
        if len(backends) == 1:
            _, backend = backends[0]
        else:
            raise ValueError(
                'You have multiple authentication backends configured and '
                'therefore must provide the `backend` argument or set the '
                '`backend` attribute on the user.'
            )
    else:
        if not isinstance(backend, str):
            raise TypeError('backend must be a dotted import path string (got %r).' % backend)

    request.session[SESSION_KEY] = account._meta.pk.value_to_string(account)
    request.session[BACKEND_SESSION_KEY] = backend
    request.session[HASH_SESSION_KEY] = session_auth_hash

    if hasattr(request, 'account'):
        request.account = account
    
    rotate_token(request)
    user_logged_in.send(sender=account.__class__, request=request, account=account)
        
