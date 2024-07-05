import secrets

from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    token = models.CharField(max_length=100, verbose_name="Токен", **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def make_token(self):
        self.token = secrets.token_hex(16)

    def set_password(self, raw_password=None):
        if raw_password:
            super().set_password(raw_password)
        else:
            raw_password = User.objects.make_random_password()
            super().set_password(raw_password)
            return raw_password
