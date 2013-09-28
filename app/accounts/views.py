from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin, SingleObjectMixin
from django.db.models import Q
from django.core.exceptions import PermissionDenied

from accounts.models import Group, User


class GroupCreateView(CreateView):
    model = Group


class GroupUpdateView(UpdateView):
    model = Group


class GroupDeleteView(DeleteView):
    model = Group


class GroupMixin(SingleObjectMixin, FormMixin):
    def get_groups_queryset(self):
        user = self.request.user
        return Group.objects.filter(Q(default_users=user) | Q(users=user))

    def get_object(self, queryset=None):
        obj = super(GroupMixin, self).get_object(queryset)
        if obj.group and not self.get_groups_queryset().filter(id=obj.group.id):
            raise PermissionDenied()
        return obj

    def get_form_class(self):
        form = super(GroupMixin, self).get_form_class()
        form.group.queryset = self.get_groups_queryset()
        return form
