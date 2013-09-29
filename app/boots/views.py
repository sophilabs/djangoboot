import json

from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, View
from django.views.generic.edit import SingleObjectMixin, ModelFormMixin
from django.views.generic.detail import BaseDetailView
from django.views.generic.base import TemplateResponseMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from boots.models import Boot, BootVersion, Star
from boots.forms import BootVersionCreationForm
from core.views import EnsureCSRFMixin
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

        self.boot = obj.boot
        return obj


class SearchView(TemplateView):
    template_name = 'boots/search.html'


class TrendingView(TemplateView):
    template_name = 'boots/trending.html'


class TeamView(TemplateView):
    template_name = 'boots/team.html'


class BootContextMixin(object):

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(BootContextMixin, self).get_context_data(**kwargs)
        context['boot'] = self.boot
        context['team_member'] = user.get_teams().filter(id=self.boot.team.id) if user.is_authenticated() else False
        return context


class BootView(EnsureCSRFMixin, BootContextMixin, BootObjectMixin, TemplateResponseMixin, BaseDetailView):
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


class BootVersionView(EnsureCSRFMixin, BootContextMixin, BootVersionObjectMixin, TemplateResponseMixin, BaseDetailView):
    template_name = 'boots/boot.html'


class StarBootView(EnsureCSRFMixin, View):

    def post(self, request, *args, **kwargs):
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
                star = Star.objects.filter(user=user, boot=boot)

                if not value:
                    if not star:
                        Star.objects.create(user=user, boot=boot)
                    response['value'] = True
                    response['message'] = _('Thank you!')
                else:
                    star.delete()
                    response['value'] = False

                response['count'] = boot.star_count
        else:
            response['message'] = _('Must be logged in.')

        return HttpResponse(json.dumps(response), content_type='application/json')
