from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, ListView, DetailView, DeleteView, UpdateView

from mailings.forms import MailingForm, MessageForm, ClientForm
from mailings.models import Mailing, Message, Client


class MainTemplateView(TemplateView):
    template_name = 'mailings/main.html'


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(owner=user)
        return queryset


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailing_list')

    def form_valid(self, form):
        if form.is_valid():
            new_mailing = form.save()
            user = self.request.user
            new_mailing.owner = user
            new_mailing.status = Mailing.CREATED
            if new_mailing.time_sending <= datetime.now().time() and new_mailing.start_mailing == datetime.now().date():
                new_mailing.next_sending = new_mailing.start_mailing + timedelta(days=1)
            else:
                new_mailing.next_sending = new_mailing.start_mailing
            new_mailing.save()
            return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse('mailings:mailing_detail', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        mailing = form.save()
        if mailing.end_mailing >= datetime.now().date() >= mailing.start_mailing:
            mailing.next_sending = datetime.now().date()
        elif mailing.end_mailing >= datetime.now().date() <= mailing.start_mailing:
            mailing.next_sending = mailing.start_mailing
        mailing.save()
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailings:mailing_list')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(owner=user)
        return queryset


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')

    def form_valid(self, form):
        if form.is_valid():
            new_message = form.save()
            user = self.request.user
            new_message.owner = user
            new_message.save()
            return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('mailings:message_detail', args=[self.kwargs.get('pk')])


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailings:message_list')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(owner=user)
        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')

    def form_valid(self, form):
        if form.is_valid():
            new_client = form.save()
            user = self.request.user
            new_client.owner = user
            new_client.save()
            return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailings:client_list')
