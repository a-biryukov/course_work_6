from django.urls import path
from mailings.apps import MailingsConfig
from mailings.views import MailingCreateView, MailingListView, CarouselTemplateView, MessageCreateView, \
    ClientCreateView, MailingDetailView, MailingDeleteView

app_name = MailingsConfig.name

urlpatterns = [
    path('', CarouselTemplateView.as_view(), name='carousel'),
    path('mailings-create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing-delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('message-create/', MessageCreateView.as_view(), name='message_create'),
    path('client-create/', ClientCreateView.as_view(), name='client_create')
    ]
