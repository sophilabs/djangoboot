from django.views.generic import CreateView, UpdateView, DeleteView

from accounts.models import Group, User


class GroupCreateView(CreateView):
    model = Group


class GroupUpdateView(UpdateView):
    model = Group


class GroupDeleteView(DeleteView):
    model = Group
