from django.views.generic import CreateView

from mailings.models import Mailing


class MailingCreateView(CreateView):
    model = Mailing
