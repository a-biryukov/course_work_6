from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from mailings.models import Mailing
from users.models import User


def email_send(obj, password=None, url=None):
    """Функция отправки сообщени по электронной почте"""
    if isinstance(obj, Mailing):
        clients = obj.clients.all()
        subject = obj.message.tittle
        message = obj.message.text,
        recipient_list = [client.email for client in clients]
    elif isinstance(obj, User) and password:
        subject = 'Восстановление пароля'
        message = f'Ваш новый пароль: {password}'
        recipient_list = [obj.email]
    elif isinstance(obj, User) and url:
        subject = 'Подтверждение почты'
        message = f'Перейдите по ссылке для подтверждения почты {url}'
        recipient_list = [obj.email]

    send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=recipient_list
    )
