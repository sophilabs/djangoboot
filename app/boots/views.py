from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, View
from django.views.generic.edit import SingleObjectMixin, ModelFormMixin
from django.views.generic.detail import BaseDetailView
from django.views.generic.base import TemplateResponseMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404

from boots.models import Boot, BootVersion
from boots.forms import BootVersionCreationForm
from accounts.views import UserTeamsMixin, TeamMixin
from boots.models import Team, Boot, BootVersion
from haystack.views import SearchView as BaseSearchView

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

        self.boot = obj.boot
        return obj


from haystack.forms import SearchForm as BaseSearchForm
from haystack.query import SearchQuerySet
from boots.search_indexes import BootIndex

class SearchForm(BaseSearchForm):
    pass


class SearchView(BaseSearchView):
    template = 'boots/search.html'
    form = SearchForm
    results = SearchQuerySet().all()
    results_per_page = 1

    @classmethod
    def as_view(cls):
        return cls()


class TrendingView(SearchView):
    template_name = 'boots/trending.html'


class TeamView(SearchView):
    template_name = 'boots/team.html'

    def __get_team(self):
        try:
            return Team.objects.get(slug=self.kwargs['team'])
        except Team.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        kwargs['team'] = self.__get_team()
        return super(TeamView, self).get_context_data(**kwargs)

    def get_queryset(self):
        return super(TeamView, self).get_queryset().filter(team=self.__get_team())


class BootContextMixin(UserTeamsMixin):

    def get_context_data(self, **kwargs):
        context = super(BootContextMixin, self).get_context_data(**kwargs)
        context['boot'] = self.boot
        context['boot_team_member'] = self.get_teams_queryset().filter(id=self.boot.team.id)
        return context


class BootView(BootContextMixin, BootObjectMixin, TemplateResponseMixin, BaseDetailView):
    template_name = 'boots/boot.html'

    def get_object(self, queryset=None):
        self.boot = super(BootView, self).get_object(queryset)
        try:
            return self.boot.versions.latest('created')
        except ObjectDoesNotExist:
            return None


class BootCreateView(TeamMixin, CreateView):
    model = Boot
    template_name = 'boots/boot_create.html'

    def get_initial(self):
        return {
            'team': self.request.user.team.id
        }


class BootUpdateView(TeamMixin, BootObjectMixin, UpdateView):
    template_name = 'boots/boot_update.html'


class BootDeleteView(TeamMixin, BootObjectMixin, DeleteView):
    template_name = 'boots/boot_delete.html'


class BootVersionCreateView(TeamMixin, CreateView):
    template_name = 'boots/boot_version_create.html'
    form_class = BootVersionCreationForm
    model = BootVersion

    def dispatch(self, request, *args, **kwargs):
        self.boot = get_object_or_404(Boot,
                                      team__slug=self.kwargs.get('team'),
                                      slug=self.kwargs.get('boot'))
        return super(BootVersionCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BootVersionCreateView, self).get_context_data(**kwargs)
        context['boot'] = self.boot
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.boot = self.boot
        self.object.save()
        return super(ModelFormMixin, self).form_valid(form)


class BootVersionDeleteView(TeamMixin, BootVersionObjectMixin, DeleteView):
    template_name = 'boots/boot_version_delete.html'


class BootVersionView(BootContextMixin, BootVersionObjectMixin, TemplateResponseMixin, BaseDetailView):
    template_name = 'boots/boot.html'
