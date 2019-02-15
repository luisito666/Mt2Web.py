import inspect
import re

from django.apps import apps as django_apps
from django.utils.module_loading import import_string 
from django.core.exceptions import ImproperlyConfigured

from core import settings

from .signals import user_logged_in, user_logged_out, user_login_failed


SESSION_KEY = '_auth_account_id'
AUTH_USER_MODEL = 'apps.authentication.models.Account'
BACKEND_SESSION_KEY = 'g1jwvO'


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


def get_user_model():
    try:
        #return import_string(AUTH_USER_MODEL)
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
        cuenta = get_user_model().objects.get(id=request.session[BACKEND_SESSION_KEY])
    except KeyError:
        cuenta = None
    
    return cuenta or AnonymousAccount()


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


def login():
    pass
