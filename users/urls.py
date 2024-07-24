from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserListView, UserCreateView, UserDetailView, UserUpdateView, UserDeleteView, \
    email_verification, PasswordRecoveryTemplateView, UserLoginView

app_name = UsersConfig.name

urlpatterns = [
    path('users/', UserListView.as_view(), name='user_list'),

    path('register/', UserCreateView.as_view(), name='register'),
    path("email-confirm/<str:token>/", email_verification, name="email_confirm"),
    path('login/', UserLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(http_method_names=['post', 'get', 'options'], template_name='users/logout.html'),name='logout'),

    path('profile/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('profile-change/<int:pk>', UserUpdateView.as_view(), name='user_update'),
    path('profile-delete/<int:pk>', UserDeleteView.as_view(), name='user_delete'),

    path('password-recovery/', PasswordRecoveryTemplateView.as_view(), name='password_recovery')
]
