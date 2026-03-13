# users/forms.py
# from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

class RegisterForm(UserCreationForm):
    class Meta:
        # model = settings.AUTH_USER_MODEL # This does not work. Use get_user_model().
        model = get_user_model() 
        fields = ["username", "email", "first_name", "last_name"] # Example of adding the email field, which is not in the default form

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model() 
        fields = ["email", "first_name", "last_name"] # Add other fields as needed
