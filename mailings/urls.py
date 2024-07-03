from django.urls import path
from mailings.apps import MailingsConfig
from mailings.views import MailingCreateView, MailingListView, CarouselTemplateView, MessageCreateView, \
    ClientCreateView, MailingDetailView, MailingDeleteView, MailingUpdateView, MessageListView, MessageDetailView, \
    MessageUpdateView, MessageDeleteView

app_name = MailingsConfig.name

urlpatterns = [
    path('', CarouselTemplateView.as_view(), name='carousel'),

    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailing-create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing-update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing-delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),

    path('messages/', MessageListView.as_view(), name='message_list'),
    path('message-create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message-update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message-delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('client-create/', ClientCreateView.as_view(), name='client_create')
    ]
