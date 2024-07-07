from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, ListView, DetailView, DeleteView, UpdateView

from mailings.forms import MailingForm, MessageForm, ClientForm, MailingModeratorForm
from mailings.models import Mailing, Message, Client, Log
from mailings.services import get_blog_from_cache, get_date_next_sending, get_status


class MainTemplateView(TemplateView):
    template_name = 'mailings/main.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        count_mailings = Mailing.objects.count()
        count_active_mailings = Mailing.objects.filter(status=Mailing.STARTED).count()
        count_unic_clients = Client.objects.values_list('email').distinct().count()
        context_data['count_mailings'] = count_mailings
        context_data['count_active_mailings'] = count_active_mailings
        context_data['count_unic_clients'] = count_unic_clients
        context_data['blog_list'] = get_blog_from_cache()
        return context_data


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset = super().get_queryset(*args, **kwargs)
        if not user.groups.filter(name='Модератор').exists():
            queryset = queryset.filter(owner=user)
        return queryset


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailing_list')

    def form_valid(self, form):
        if form.is_valid():
            mailing = form.save()
            user = self.request.user
            mailing.owner = user
            mailing.next_sending = get_date_next_sending(mailing)
            mailing.status = get_status(mailing)
            mailing.save()
            return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.groups.filter(name='Модератор').exists():
            return self.object
        raise PermissionDenied


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse('mailings:mailing_detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingForm
        elif user.groups.filter(name='Модератор').exists():
            return MailingModeratorForm
        raise PermissionDenied

    def form_valid(self, form):
        mailing = form.save()
        mailing.next_sending = get_date_next_sending(mailing)
        mailing.status = get_status(mailing)
        mailing.save()
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailings:mailing_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


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

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            return self.object
        raise PermissionDenied


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('mailings:message_detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MessageForm
        raise PermissionDenied


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailings:message_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


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


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            return self.object
        raise PermissionDenied


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('mailings:client_detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ClientForm
        raise PermissionDenied


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailings:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class LogListView(LoginRequiredMixin, ListView):
    model = Log

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(mailing__owner=user.pk).order_by('time')
        return queryset
