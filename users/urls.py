from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateView, RecoveryTemplateView, UserDetailView, UserUpdateView, UserDeleteView, \
    email_verification

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(http_method_names=['post', 'get', 'options'], template_name='users/logout.html'),name='logout'),
    path('password-recovery/', RecoveryTemplateView.as_view(), name='password_recovery'),
    path('profile/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('profile-change/<int:pk>', UserUpdateView.as_view(), name='user_update'),
    path('profile-delete/<int:pk>', UserDeleteView.as_view(), name='user_delete'),
    path("email-confirm/<str:token>/", email_verification, name="email_confirm")
]
