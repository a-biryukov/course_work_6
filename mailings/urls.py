from django.urls import path
from mailings.apps import MailingsConfig
from mailings.views import MailingCreateView

app_name = MailingsConfig.name

urlpatterns = [
    path("mailing", MailingCreateView.as_view(), name="mailing")
    ]
