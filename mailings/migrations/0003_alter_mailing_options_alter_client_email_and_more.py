# Generated by Django 5.0.6 on 2024-07-04 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailing',
            options={'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=100, verbose_name='Почта'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='clients',
            field=models.ManyToManyField(help_text='Для выбора нескольких клиентов удерживате CTRL', related_name='clients', to='mailings.client', verbose_name='Клиенты для рассылки'),
        ),
    ]
