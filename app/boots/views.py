from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.views.generic.edit import SingleObjectMixin, ModelFormMixin
from django.views.generic.detail import BaseDetailView
from django.views.generic.base import TemplateResponseMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.utils.translation import ugettext as _

from haystack.views import SearchView as BaseSearchView
from haystack.query import SearchQuerySet

from boots.models import Boot, BootVersion, Star
from boots.forms import BootForm, BootVersionForm, SearchForm
from accounts.views import TeamOnlyMixin, TeamObjectMixin
from core.views import EnsureCSRFMixin, JSONResponseMixin


class BootObjectMixin(SingleObjectMixin):
    model = Boot
    context_object_name = 'boot'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        try:
            obj = queryset.get(team__slug=self.kwargs.get('team'),
                               slug=self.kwargs.get('boot'))
        except ObjectDoesNotExist:
            raise Http404

        self.boot = obj

        return obj


class BootVersionObjectMixin(SingleObjectMixin):
    model = BootVersion
    context_object_name = 'version'

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


class SearchView(BaseSearchView):
    template = 'boots/search.html'

    def build_form(self, form_kwargs=None):
        kwargs = {'sort': 'loved'}
        if form_kwargs:
            kwargs.update(form_kwargs)
        return super(SearchView, self).build_form(kwargs)

    def extra_context(self):
        extra = super(SearchView, self).extra_context()
        facets = self.results.facet_counts()
        tags = facets['fields']['tags'] if facets and facets.get('fields', None) and facets['fields'].get('tags', None) else []
        facet_tags = [tag[0] for tag in tags]
        filter_tags = self.form.tags
        tags = [(tag[0], tag[1], tag[0] in filter_tags,) for tag in tags]
        filter_tags = filter(lambda tag: tag not in facet_tags, filter_tags)
        tags = [(tag, 0, True) for tag in filter_tags] + tags
        extra['tags'] = tags
        return extra

    @classmethod
    def as_view(cls):
        return cls(
            load_all=True,
            form_class=SearchForm,
            searchqueryset=SearchQuerySet().models(Boot),
            results_per_page=20)


class TrendingView(SearchView):
    template = 'boots/trending.html'

    def build_form(self, form_kwargs=None):
        kwargs = {'sort': 'today'}
        if form_kwargs:
            kwargs.update(form_kwargs)
        return super(TrendingView, self).build_form(kwargs)

class TeamView(TeamObjectMixin, SearchView):
    template = 'boots/team.html'

    def extra_context(self):
        extra = super(TeamView, self).extra_context()
        extra['team'] = self.get_object()
        return extra

    def __call__(self, request, team):
        self.kwargs = {'team': team}
        return super(TeamView, self).__call__(request)


class BootContextMixin(object):

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(BootContextMixin, self).get_context_data(**kwargs)
        context['boot'] = self.boot
        context['team_member'] = user.get_teams().filter(id=self.boot.team.id) if user.is_authenticated() else False
        return context


class BootView(EnsureCSRFMixin, BootContextMixin, BootObjectMixin, TemplateResponseMixin, BaseDetailView):
    template_name = 'boots/boot.html'
    context_object_name = 'version'

    def get_object(self, queryset=None):
        super(BootView, self).get_object(queryset)
        try:
            return self.boot.versions.latest()
        except ObjectDoesNotExist:
            return None


class BootCreateView(TeamOnlyMixin, CreateView):
    template_name = 'boots/boot_create.html'
    form_class = BootForm
    model = Boot

    def get_initial(self):
        return {
            'team': self.request.user.team.id
        }


class BootUpdateView(TeamOnlyMixin, BootObjectMixin, UpdateView):
    template_name = 'boots/boot_update.html'
    form_class = BootForm


class BootDeleteView(TeamOnlyMixin, BootObjectMixin, DeleteView):
    template_name = 'delete.html'

    def get_success_url(self):
        return self.request.user.get_absolute_url()


class BootVersionCreateView(TeamOnlyMixin, CreateView):
    template_name = 'boots/boot_version_create.html'
    form_class = BootVersionForm
    model = BootVersion

    def get_form(self, form_class):
        self.boot = Boot.objects.get(team__slug=self.kwargs.get('team'),
                                     slug=self.kwargs.get('boot'))

        form = super(BootVersionCreateView, self).get_form(form_class)
        form.boot = self.boot
        return form

    def get_context_data(self, **kwargs):
        context = super(BootVersionCreateView, self).get_context_data(**kwargs)
        context['boot'] = self.boot
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.boot = self.boot
        self.object.save()
        return super(BootVersionCreateView, self).form_valid(form)


class BootVersionDeleteView(TeamOnlyMixin, BootVersionObjectMixin, DeleteView):
    template_name = 'delete.html'

    def get_success_url(self):
        return self.object.boot.get_absolute_url()


class BootVersionView(EnsureCSRFMixin, BootContextMixin, BootVersionObjectMixin, TemplateResponseMixin, BaseDetailView):
    template_name = 'boots/boot.html'


class StarBootView(JSONResponseMixin, EnsureCSRFMixin, View):

    def json_post(self, request, *args, **kwargs):
        user = request.user

        response = {}

        if user.is_authenticated():
            boot_id = request.POST.get('boot_id')
            try:
                boot = Boot.objects.get(id=boot_id)
            except ObjectDoesNotExist:
                boot = None
                response['message'] = _('Boot not found.')

            if boot:
                value = request.POST.get('value') == 'true'
                try:
                    star = Star.objects.get(user=user, boot=boot)
                except Star.DoesNotExist:
                    star = None

                if not value:
                    if not star:
                        Star.objects.create(user=user, boot=boot)
                    response['value'] = True
                    response['message'] = _('Thank you!')
                else:
                    if star:
                        star.delete()
                    response['value'] = False

                response['count'] = Boot.objects.get(id=boot_id).star_count
        else:
            response['message'] = _('Must be logged in.')

        return response
