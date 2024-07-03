from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from users.forms import UserRegisterForm, RecoveryForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")


class RecoveryTemplateView(TemplateView):
    template_name = 'users/password_recovery.html'
    form_class = RecoveryForm
    success_url = reverse_lazy("users:login")