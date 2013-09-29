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
    include_users = True
    include_teams = True

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        try:
            obj = queryset.get(slug=self.kwargs['team'])
        except ObjectDoesNotExist:
            raise Http404

        if not self.include_users:
            if User.objects.filter(team=obj):
                raise Http404()

        if not self.include_teams:
            if User.objects.filter(teams=obj):
                raise Http404()

        return obj


class UserDetailsView(LoginRequiredMixin, TeamObjectMixin, UpdateView):
    model = Team
    template_name = 'accounts/user_details.html'
    include_teams = False


class TeamMixin(LoginRequiredMixin, TeamObjectMixin):

    def get_object(self, queryset=None):
        obj = super(TeamMixin, self).get_object(queryset)
        if not self.request.user.get_teams().filter(id=obj.id):
            raise PermissionDenied()
        return obj


class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    template_name = 'accounts/team_create.html'

    def form_valid(self, form):
        self.object = form.save()
        self.request.user.teams.add(self.object)
        return super(TeamCreateView, self).form_valid(form)


class TeamUpdateView(TeamMixin, UpdateView):
    model = Team
    template_name = 'accounts/team_update.html'
    include_users = False


class TeamDeleteView(TeamMixin, DeleteView):
    model = Team
    template_name = 'delete.html'
    include_users = False


class TeamOnlyMixin(LoginRequiredMixin, FormMixin, SingleObjectMixin):

    def get_teams_queryset(self):
        return self.request.user.get_teams()

    def get_object(self, queryset=None):
        obj = super(TeamOnlyMixin, self).get_object(queryset)
        if obj.team and not self.get_teams_queryset().filter(id=obj.team.id):
            raise PermissionDenied()
        return obj

    def get_form(self, form_class):
        form = super(TeamOnlyMixin, self).get_form(form_class)
        team_field = form.fields.get('team')
        if team_field:
            team_field.queryset = self.get_teams_queryset()
            team_field.widget = forms.HiddenInput()
        return form
