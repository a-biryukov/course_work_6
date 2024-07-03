from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateView, RecoveryTemplateView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(http_method_names=["post", "get", "options"], template_name="users/logout.html"),name="logout"),
    path("password-recovery/", RecoveryTemplateView.as_view(), name="password_recovery")
]
