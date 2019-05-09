
from apps.authentication import get_user_model


UserModel = get_user_model()


class ModelBackend:
    """
    Autentica con la configuracion 
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel.objects.get(login=username)
        except UserModel.DoesNotExist:
            UserModel().set_password()
        else:
            if user.check_password(password) and not user.is_banned:
                return user
    
    def user_can_authenticate(self, user):
        is_banned = getattr(user, 'is_banned', None)
        return is_banned or is_banned is None
    
    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if not user.is_banned and self.user_can_authenticate(user) else None

