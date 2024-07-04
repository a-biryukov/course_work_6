from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView, DeleteView

from users.forms import UserRegisterForm, UserUpdateForm, PasswordRecoveryForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.make_token()
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{user.token}/'
        user.email_send(subject="Подтверждение почты", message=f'Перейдите по ссылке для подтверждения почты {url}')
        return super().form_valid(form)


class UserDetailView(LoginRequiredMixin,DetailView):
    model = User


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users:register')


class PasswordRecoveryTemplateView(TemplateView):
    template_name = 'users/password_recovery.html'
    form_class = PasswordRecoveryForm
    success_url = reverse_lazy('users:login')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        if User.objects.filter(email=email):
            user = User.objects.get(email=email)
            password = user.set_password()
            user.save()
            user.email_send(subject='Восстановление пароля', message=f'Ваш новый пароль: {password}')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["form"] = self.form_class
        return context_data


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))
