import smtplib
from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.cache import cache
from django.core.mail import send_mail

from blog.models import Blog
from config.settings import EMAIL_HOST_USER, CACHE_ENABLED, TIME_ZONE
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


def start_mailing() -> None:
    """Функция старта рассылок"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=10)
    scheduler.start()


def send_mailing() -> None:
    """
    Получает подходящие по дате рассылки, устанавливает статус 'Запущена' или 'Завершена',
    отправляет сообщения, устанавливает дату следующей отправки и сохраняет логи
    """
    zone = pytz.timezone(TIME_ZONE)
    current_datetime = datetime.now(zone)
    current_date = current_datetime.date()
    current_time = current_datetime.time()

    mailings = Mailing.objects.filter(
        start_mailing__lte=current_date,
        end_mailing__gte=current_date
    )

    for mailing in mailings:
        mailing.status = get_status(mailing)
        if mailing.next_sending == current_date and mailing.time_sending <= current_time:
            try:
                server_response = email_send(mailing, fail_silently=False)
            except smtplib.SMTPException as e:
                server_response = e
                status = False
            else:
                mailing.next_sending = change_date_next_sending(mailing)
                status = True
            finally:
                Log.objects.create(status=status, server_response=server_response, mailing=mailing)
        mailing.save()


def get_status(obj) -> str:
    """Проверяет дату и возвращает соответствующий статус 'Запущена' или 'Завершена'"""
    zone = pytz.timezone(TIME_ZONE)
    current_datetime = datetime.now(zone)
    current_date = current_datetime.date()
    current_time = current_datetime.time()
    start_date = obj.start_mailing
    end_date = obj.end_mailing
    time_sending = obj.time_sending

    if (end_date > current_date > start_date or
            end_date > current_date == start_date and time_sending < current_time or
            end_date == current_date and time_sending > current_time or
            start_date == current_date and time_sending > current_time):
        return Mailing.STARTED
    elif end_date == current_date and current_time > time_sending or current_date > end_date:
        return Mailing.COMPLETED
    else:
        return Mailing.CREATED


def change_date_next_sending(obj):
    """Меняет дату следующей отправки в зависимости от выбранной пользователем периодичности"""
    if obj.periodicity == Mailing.DAILY:
        return obj.next_sending + timedelta(days=1)
    elif obj.periodicity == Mailing.WEEKLY:
        return obj.next_sending + timedelta(weeks=1)
    elif obj.periodicity == Mailing.MONTHLY:
        return obj.next_sending + timedelta(days=30)


def get_blog_from_cache():
    """ Получает статьи из кеша, если кеш пуст получает из БД"""
    if not CACHE_ENABLED:
        return Blog.objects.order_by('?')[:3]

    key = 'blog_list'
    blog_list = cache.get(key)
    if blog_list is None:
        blog_list = Blog.objects.order_by('?')[:3]
        cache.set(key, blog_list)
    return blog_list


def get_date_next_sending(obj):
    """Gjkexftn """
    zone = pytz.timezone(TIME_ZONE)
    current_datetime = datetime.now(zone)
    current_date = current_datetime.date()
    current_time = current_datetime.time()
    start_date = obj.start_mailing
    end_date = obj.end_mailing
    time_sending = obj.time_sending

    if start_date > current_date:
        return start_date
    elif start_date <= current_date < end_date and time_sending < current_time:
        return current_date + timedelta(days=1)
    else:
        return current_date
