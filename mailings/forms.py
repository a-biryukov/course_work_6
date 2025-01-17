from django.forms import BooleanField, ModelForm

from mailings.models import Mailing, Message, Client


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class MailingForm(StyleFormMixin, ModelForm):

    class Meta:
        model = Mailing
        exclude = ('owner', 'status', 'next_sending', 'is_active')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        user = self.request.user
        super().__init__(*args, **kwargs)
        self.fields['clients'].queryset = Client.objects.filter(owner=user)
        self.fields['message'].queryset = Message.objects.filter(owner=user)


class MailingModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        fields = ('is_active',)


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        exclude = ('owner',)


class ClientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        exclude = ('owner',)
