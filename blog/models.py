from django.db import models

from config.settings import NULLABLE
from users.models import User


class Blog(models.Model):
    tittle = models.CharField(max_length=100, verbose_name='Заголовок', help_text='Введите заголовок')
    text = models.TextField(verbose_name='Текст', help_text='Введите текст')
    image = models.ImageField(upload_to='blog/images', **NULLABLE, verbose_name='Изображение', help_text='Загрузите изображение')
    created_at = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    author = models.ForeignKey(User, verbose_name="Автор", help_text="Введите автора", **NULLABLE, on_delete=models.SET_NULL)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    views_count = models.IntegerField(default=0, verbose_name=' Просмотры')
    slug = models.CharField(max_length=100, verbose_name='Slug', **NULLABLE)

    def __str__(self):
        return self.tittle

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        permissions = [
            ('can_edit_publication', 'Can edit publication'),
            ('can_edit_tittle', 'Can edit tittle'),
            ('can_edit_text', 'Can edit text'),
            ('can_edit_image', 'Can edit image')
        ]

