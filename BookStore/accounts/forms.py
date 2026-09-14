from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ["username", "email", "phone_number"]