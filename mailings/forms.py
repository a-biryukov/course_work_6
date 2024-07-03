from django.forms import BooleanField, ModelForm, DateTimeField, DateInput

from mailings.models import Mailing


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
        exclude = ("owner",)
