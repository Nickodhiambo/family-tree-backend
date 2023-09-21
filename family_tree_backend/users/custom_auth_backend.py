from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailorUsername(ModelBackend):
    """Authenticates using email or password"""
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        #check if username is an email
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}

        #Checks if username exists
        try:
            user = UserModel.objects.get(**kwargs)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        """For session management after login"""
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
