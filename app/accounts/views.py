from django.views.generic import CreateView, UpdateView

from accounts.models import Group, User


class GroupCreateView(CreateView):
    model = Group


class GroupUpdateView(UpdateView):
    model = Group


class GroupDeleteView(UpdateView):
    model = Group
