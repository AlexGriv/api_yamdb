from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class CustomBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        username = kwargs['username']
        confirmation_code = kwargs['confirmation_code']
        try:
            user = User.objects.get(
                username=username, confirmation_code=confirmation_code)
            if user:
                return user
        except User.DoesNotExist:
            pass
