from django.urls import path
from mailings.apps import MailingsConfig
from mailings.views import MainTemplateView, MailingListView, MailingCreateView, \
    MailingDetailView, MailingUpdateView, MailingDeleteView, MessageListView, MessageCreateView, MessageDetailView, \
    MessageUpdateView, MessageDeleteView, ClientListView, ClientCreateView, ClientDetailView, ClientUpdateView, \
    ClientDeleteView

app_name = MailingsConfig.name

urlpatterns = [
    path('', MainTemplateView.as_view(), name='main'),

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

    path('clients/', ClientListView.as_view(), name='client_list'),
    path('client-create/', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client-update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client-delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete')
]
