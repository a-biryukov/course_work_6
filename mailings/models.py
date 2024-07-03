from django.db import models

from config.settings import NULLABLE
from users.models import User


class Client(models.Model):
    email = models.EmailField(max_length=100, verbose_name='Почта', unique=True)
    name = models.CharField(max_length=100, verbose_name='Имя')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f'{self.name, self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    tittle = models.CharField(max_length=150, verbose_name='Тема сообщения')
    text = models.TextField(verbose_name='Текст сообщения')
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return self.tittle

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    DAILY = 'Раз в день'
    WEEKLY = 'Раз в неделю'
    MONTHLY = 'Раз в месяц'

    PERIODICITY_CHOICES = [
        (DAILY, 'Раз в день'),
        (WEEKLY, 'Раз в неделю'),
        (MONTHLY, 'Раз в месяц'),
    ]

    CREATED = 'Создана'
    STARTED = 'Запущена'
    COMPLETED = 'Завершена'

    STATUS_CHOICES = [
        (COMPLETED, 'Завершена'),
        (CREATED, 'Создана'),
        (STARTED, 'Запущена'),
    ]

    start_mailing = models.DateTimeField(verbose_name='Дата и время первой отправки')
    end_mailing = models.DateTimeField(verbose_name='Дата и время окончания рассылки')
    periodicity = models.CharField(
        max_length=150,
        choices=PERIODICITY_CHOICES,
        default=DAILY,
        verbose_name="Периодичность рассылки",
    )
    status = models.CharField(
        max_length=150,
        choices=STATUS_CHOICES,
        default=CREATED,
        verbose_name="Статус рассылки"
    )
    clients = models.ManyToManyField(
        Client, related_name='mailing',
        verbose_name='Клиенты для рассылки',
        help_text='Для выбора нескольких клиентов удерживате CTRL'
    )
    message = models.ForeignKey(Message, verbose_name='Cообщение', on_delete=models.CASCADE, **NULLABLE)
    owner = models.ForeignKey(User, verbose_name='Владелец',  on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f'{self.periodicity} c {self.start_mailing} по {self.end_mailing}, рассылка {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Log(models.Model):
    time = models.DateTimeField(verbose_name='Дата и время попытки отправки', auto_now_add=True)
    status = models.BooleanField(verbose_name='Статус попытки отправки')
    server_response = models.CharField(max_length=150, verbose_name='Ответ почтового сервера', **NULLABLE)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')

    def __str__(self):
        return f' {self.time}, {self.status}, {self.server_response}'

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
