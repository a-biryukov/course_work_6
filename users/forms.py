from django.contrib.auth.forms import UserCreationForm
from django import forms

from mailings.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ("email", "password1", "password1")


class RecoveryForm(StyleFormMixin, forms.Form):
    email = forms.EmailField(max_length=255)
