from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms

from mailings.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password1')


class UserUpdateForm(StyleFormMixin, UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)


class UserModeratorUpdateForm(StyleFormMixin, UserChangeForm):

    class Meta:
        model = User
        fields = ('is_active',)


class PasswordRecoveryForm(StyleFormMixin, forms.Form):
    email = forms.EmailField(max_length=255)


class UserAuthenticationForm(StyleFormMixin, AuthenticationForm):
    pass
