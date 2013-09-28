from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import SingleObjectMixin, ModelFormMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404

from boots.models import Boot, BootVersion
from accounts.views import TeamMixin


class BootObjectMixin(SingleObjectMixin):
    model = Boot

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        try:
            obj = queryset.get(team__slug=self.kwargs.get('team'),
                               slug=self.kwargs.get('boot'))
        except ObjectDoesNotExist:
            raise Http404

        return obj


class BootVersionObjectMixin(SingleObjectMixin):
    model = BootVersion

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        try:
            obj = queryset.get(boot__team__slug=self.kwargs.get('team'),
                               boot__slug=self.kwargs.get('boot'),
                               slug=self.kwargs.get('version'))
        except ObjectDoesNotExist:
            raise Http404

        return obj


class SearchView(TemplateView):
    template_name = 'boots/search.html'


class TrendingView(TemplateView):
    template_name = 'boots/trending.html'


class TeamView(TemplateView):
    template_name = 'boots/team.html'


class BootView(TemplateView):
    template_name = 'boots/boot.html'


class BootCreateView(TeamMixin, CreateView):
    model = Boot
    template_name = 'boots/boot_create.html'


class BootUpdateView(TeamMixin, BootObjectMixin, UpdateView):
    template_name = 'boots/boot_update.html'


class BootDeleteView(TeamMixin, BootObjectMixin, DeleteView):
    template_name = 'boots/boot_delete.html'


class BootVersionCreateView(TeamMixin, BootVersionObjectMixin, CreateView):
    template_name = 'boots/boot_version_create.html'
    fields = ['slug', 'source']

    def dispatch(self, request, *args, **kwargs):
        self.boot = get_object_or_404(Boot,
                                      team__slug=self.kwargs.get('team'),
                                      slug=self.kwargs.get('boot'))
        return super(BootVersionCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.boot = self.boot
        self.object.save()
        return super(ModelFormMixin, self).form_valid(form)


class BootVersionDeleteView(TeamMixin, BootVersionObjectMixin, DeleteView):
    template_name = 'boots/boot_version_delete.html'


class BootVersionView(TemplateView):
    template_name = 'boots/boot_version.html'
