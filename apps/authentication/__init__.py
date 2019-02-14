from django.utils.module_loading import import_string 
from django.core.exceptions import ImproperlyConfigured


SESSION_KEY = '_auth_account_id'
AUTH_USER_MODEL = 'apps.authentication.models.Account'
BACKEND_SESSION_KEY = '_auth_user_backend'


def get_user_model():
    try:
        return import_string(AUTH_USER_MODEL)
    except ValueError:
        raise ImproperlyConfigured("AUTH_USER_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL refers to model '%s' that has not been installed" % settings.AUTH_USER_MODEL
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

