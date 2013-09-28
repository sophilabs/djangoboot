from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin, SingleObjectMixin
from django.db.models import Q
from django.core.exceptions import PermissionDenied

from accounts.models import Group, User


class GroupCreateView(CreateView):
    model = Group
    template_name = 'accounts/group_create.html'


class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'accounts/group_update.html'


class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'accounts/group_delete.html'


class GroupMixin(FormMixin, SingleObjectMixin):
    def get_groups_queryset(self):
        user = self.request.user
        return Group.objects.filter(Q(default_users=user) | Q(users=user))

    def get_object(self, queryset=None):
        obj = super(GroupMixin, self).get_object(queryset)
        if obj.group and not self.get_groups_queryset().filter(id=obj.group.id):
            raise PermissionDenied()
        return obj

    def get_form(self):
        form = super(GroupMixin, self).get_form()
        if hasattr(form, 'group'):
            form.group.queryset = self.get_groups_queryset()
        return form
