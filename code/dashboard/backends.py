from django.contrib.auth.backends import ModelBackend
from .models import Users

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            # Look for the user in your custom Users table using the email
            user = Users.objects.get(user_email=email)
            # Verify the hashed password
            if user.check_password(password):
                return user
        except Users.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None