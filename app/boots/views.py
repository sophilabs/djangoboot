from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import SingleObjectMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from boots.models import Boot, BootVersion
from accounts.views import GroupMixin


class SearchView(TemplateView):
    template_name = 'boots/search.html'


class TrendingView(TemplateView):
    template_name = 'boots/trending.html'


class GroupView(TemplateView):
    template_name = 'boots/group.html'


class BootView(TemplateView):
    template_name = 'boots/boot.html'


class BootCreateView(GroupMixin, CreateView):
    model = Boot
    template_name = 'boots/boot_create.html'


class BootObjectMixin(SingleObjectMixin):
    model = Boot

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        try:
            obj = queryset.get(group__slug=self.kwargs.get('group'),
                               slug=self.kwargs.get('boot'))
        except ObjectDoesNotExist:
            raise Http404

        return obj


class BootUpdateView(GroupMixin, BootObjectMixin, UpdateView):
    template_name = 'boots/boot_update.html'


class BootDeleteView(GroupMixin, BootObjectMixin, DeleteView):
    template_name = 'boots/boot_delete.html'


class BootVersionObjectMixin(SingleObjectMixin):
    model = BootVersion

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        try:
            obj = queryset.get(boot__group__slug=self.kwargs.get('group'),
                               boot__slug=self.kwargs.get('boot'),
                               slug=self.kwargs.get('version'))
        except ObjectDoesNotExist:
            raise Http404

        return obj


class BootVersionCreateView(CreateView):
    template_name = 'boots/boot_version_create.html'
    fields = ['slug', 'source']


class BootVersionDeleteView(DeleteView):
    template_name = 'boots/boot_version_delete.html'


class BootVersionView(TemplateView):
    template_name = 'boots/boot_version.html'
