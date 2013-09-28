from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.views.generic.edit import FormMixin, SingleObjectMixin
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout
from django.shortcuts import redirect
from django import forms

from core.views import LoginRequiredMixin
from accounts.models import Team, User


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(request.GET.get('next', 'home:index'))


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
        user = self.request.user
        return Team.objects.filter(Q(default_users=user) | Q(users=user))

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
