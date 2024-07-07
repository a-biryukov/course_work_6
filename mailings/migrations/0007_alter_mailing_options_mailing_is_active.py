# Generated by Django 5.0.6 on 2024-07-06 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0006_alter_mailing_end_mailing_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailing',
            options={'permissions': [('can_view_mailing', 'Can view mailing'), ('can_disable_mailing', 'Can disable mailing')], 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
        migrations.AddField(
            model_name='mailing',
            name='is_active',
            field=models.BooleanField(db_default=True, verbose_name='Активная'),
        ),
    ]
