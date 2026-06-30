from django.contrib.auth.backends import BaseBackend
from .models import User


class MobileBackend(BaseBackend):

    def authenticate(self, request, mobile=None, password=None, **kwargs):

        if mobile is None or password is None:
            return None

        try:
            user = User.objects.get(mobile=mobile)

        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None

    def user_can_authenticate(self, user):
        return user.is_active

    def get_user(self, user_id):

        try:
            return User.objects.get(pk=user_id)

        except User.DoesNotExist:
            return None