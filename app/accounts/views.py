from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.views.generic.edit import FormMixin, SingleObjectMixin
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import Http404
from django.contrib.auth import logout
from django.shortcuts import redirect
from django import forms

from core.views import LoginRequiredMixin
from accounts.models import Team, User


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(request.GET.get('next', 'home:index'))


class TeamObjectMixin(SingleObjectMixin):
    model = Team
    context_object_name = 'team'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        try:
            obj = queryset.get(slug=self.kwargs['team'])
        except ObjectDoesNotExist:
            raise Http404

        return obj


class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    template_name = 'accounts/team_create.html'


class TeamUpdateView(LoginRequiredMixin, UpdateView):
    model = Team
    template_name = 'accounts/team_update.html'


class TeamDeleteView(LoginRequiredMixin, DeleteView):
    model = Team
    template_name = 'accounts/team_delete.html'


class TeamMixin(LoginRequiredMixin, FormMixin, SingleObjectMixin):

    def get_teams_queryset(self):
        return self.request.user.get_teams()

    def get_object(self, queryset=None):
        obj = super(TeamMixin, self).get_object(queryset)
        if obj.team and not self.get_teams_queryset().filter(id=obj.team.id):
            raise PermissionDenied()
        return obj

    def get_form(self, form_class):
        form = super(TeamMixin, self).get_form(form_class)
        team_field = form.fields.get('team')
        if team_field:
            team_field.queryset = self.get_teams_queryset()
            team_field.widget = forms.HiddenInput()
        return form
