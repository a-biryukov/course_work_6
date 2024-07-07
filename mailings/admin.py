from django.contrib import admin

from mailings.models import Client, Message, Mailing


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'comment', 'owner')
    search_fields = ('email', 'owner')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('tittle', 'text', 'owner')
    search_fields = ('tittle', 'text', 'owner')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('start_mailing', 'end_mailing', 'periodicity', 'status')
    search_fields = ('tittle', 'text', 'owner')
