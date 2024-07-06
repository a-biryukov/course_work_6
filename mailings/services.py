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


def start() -> None:
    """Функция старта рассылок"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=10)
    scheduler.start()


def send_mailing() -> None:
    """
    Получает подходящие по дате рассылки, устанавливает статус 'Запущена' или 'Завершена',
    отправляет сообщения, устанавливает дату следующей отправки и сохраняет логи
    """
    current_date = datetime.now().date()
    current_time = datetime.now().time()

    mailings = Mailing.objects.filter(
        start_mailing__lte=current_date,
        end_mailing__gte=current_date
    )

    for mailing in mailings:
        make_status(mailing)
        if mailing.next_sending == current_date and mailing.time_sending <= current_time:
            try:
                server_response = email_send(mailing, fail_silently=False)
            except smtplib.SMTPException as e:
                server_response = e
                status = False
            else:
                change_date_next_sending(mailing)
                status = True
            finally:
                Log.objects.create(status=status, server_response=server_response, mailing=mailing)


def make_status(obj) -> None:
    """Проверяет дату и устанавливает соответствующий статус 'Запущена' или 'Завершена'"""
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    start_date = obj.start_mailing
    end_date = obj.end_mailing
    time_sending = obj.time_sending

    if (end_date > current_date > start_date or
            end_date > current_date == start_date and time_sending < current_time or
            end_date == current_date and time_sending > current_time or
            start_date == current_date and time_sending > current_time):
        obj.status = Mailing.STARTED
    elif end_date == current_date and current_time > time_sending or current_date > end_date:
        obj.status = Mailing.COMPLETED
    obj.save()


def change_date_next_sending(obj) -> None:
    """Меняет дату следующей отправки в зависимости от выбранной пользователем периодичности"""
    if obj.periodicity == Mailing.DAILY:
        obj.next_sending += timedelta(days=1)
    elif obj.periodicity == Mailing.WEEKLY:
        obj.next_sending += timedelta(weeks=1)
    elif obj.periodicity == Mailing.MONTHLY:
        obj.next_sending += timedelta(days=30)
    obj.save()
