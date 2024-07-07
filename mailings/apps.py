from time import sleep

from django.apps import AppConfig


class MailingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailings'

    def ready(self):
        from mailings.services import start_mailing
        sleep(2)
        start_mailing()
