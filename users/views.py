from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView, DeleteView, ListView

from mailings.services import email_send
from users.forms import UserRegisterForm, UserUpdateForm, PasswordRecoveryForm, UserModeratorUpdateForm
from users.models import User


class UserListView(ListView):
    model = User

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_staff=False, is_superuser=False)
        return queryset


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
        email_send(user, url=url)
        return super().form_valid(form)


class UserDetailView(LoginRequiredMixin,DetailView):
    model = User

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.email == self.object.email or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'

    def get_form_class(self):
        user = self.request.user
        if user.email == self.object.email:
            self.success_url = reverse('users:user_detail', args=[self.kwargs.get('pk')])
            return UserUpdateForm
        elif user.groups.filter(name='Модератор').exists():
            self.success_url = reverse_lazy('users:user_list')
            return UserModeratorUpdateForm
        raise PermissionDenied


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users:register')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.email == self.object.email or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


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
            email_send(user, password=password)
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
