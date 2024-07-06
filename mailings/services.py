import smtplib
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from mailings.models import Mailing, Log
from users.models import User


def email_send(obj, password=None, url=None, fail_silently=True):
    """Функция отправки сообщений по электронной почте"""
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

    server_response = send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=fail_silently
    )
    if not fail_silently:
        return server_response


def start():
    """Функция старта рассылок"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=10)
    scheduler.start()


def send_mailing():
    """Проверяет дату, время, отправляет сообщение, если нужно и сохраняет логи"""
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    mailings = Mailing.objects.filter(
        start_mailing__lte=current_date,
        end_mailing__gte=current_date
    )

    for mailing in mailings:
        if mailing.status != Mailing.STARTED and mailing.end_mailing >= current_date >= mailing.start_mailing :
            mailing.status = Mailing.STARTED
            mailing.save()

        if mailing.next_sending == current_date and mailing.time_sending <= current_time:
            try:
                server_response = email_send(mailing, fail_silently=False)
            except smtplib.SMTPException as e:
                server_response = e
                status = False
            else:

                if mailing.end_mailing == current_date and mailing.time_sending <= current_time:
                    mailing.status = Mailing.COMPLETED
                    mailing.save()

                if mailing.periodicity == mailing.DAILY:
                    mailing.next_sending += timedelta(days=1)
                elif mailing.periodicity == mailing.WEEKLY:
                    mailing.next_sending += timedelta(weeks=1)
                elif mailing.periodicity == mailing.MONTHLY:
                    mailing.next_sending += timedelta(days=30)
                mailing.save()
                status = True

            finally:
                Log.objects.create(status=status, server_response=server_response, mailing=mailing)
