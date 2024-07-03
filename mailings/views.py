from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, DetailView, DeleteView

from mailings.forms import MailingForm, MessageForm, ClientForm
from mailings.models import Mailing, Message, Client


class MailingListView(ListView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailing_list')


class MailingDetailView(DetailView):
    model = Mailing


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:client_create')


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:mailing_create')


class CarouselTemplateView(TemplateView):
    template_name = 'mailings/carousel.html'
