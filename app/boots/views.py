from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from boots.models import Boot, BootVersion
from accounts.views import GroupMixin


class SearchView(TemplateView):
    template_name = 'boots/search.html'


class BootCreateView(GroupMixin, CreateView):
    model = Boot


class BootUpdateView(GroupMixin, UpdateView):
    model = Boot


class BootDeleteView(GroupMixin, DeleteView):
    model = Boot
