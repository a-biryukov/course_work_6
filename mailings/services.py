from datetime import datetime

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER, TIME_ZONE
from mailings.models import Mailing
from users.models import User


def email_send(obj, password=None, url=None):
    """Функция отправки сообщени по электронной почте"""
    if isinstance(obj, Mailing):
        clients = obj.clients.all()
        subject = obj.message.tittle
        message = obj.message.text
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


def start():
    """Функция старта рассылок"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=10)
    scheduler.start()


def send_mailing():
    zone = pytz.timezone(TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Mailing.objects.filter(start_mailing__lte=current_datetime, end_mailing__gte=current_datetime)
    mailings_completed = Mailing.objects.filter(end_mailing__lte=current_datetime).filter(
        status__in=[Mailing.CREATED,Mailing.STARTED])

    for mailing in mailings_completed:
        mailing.status = Mailing.COMPLETED
        mailing.save()

    for mailing in mailings:
        if mailing.status != Mailing.STARTED:
            mailing.status = Mailing.STARTED
            mailing.save()

