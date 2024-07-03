from django.urls import path
from mailings.apps import MailingsConfig
from mailings.views import MailingCreateView, MailingListView, CarouselTemplateView

app_name = MailingsConfig.name

urlpatterns = [
    path("", CarouselTemplateView.as_view(), name="carousel"),
    path("create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailings/", MailingListView.as_view(), name="mailing_list")
    ]
