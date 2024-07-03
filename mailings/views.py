from django.views.generic import CreateView, TemplateView, ListView

from mailings.forms import MailingForm
from mailings.models import Mailing


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm


class MailingListView(ListView):
    model = Mailing


class CarouselTemplateView(TemplateView):
    template_name = 'mailings/carousel.html'
