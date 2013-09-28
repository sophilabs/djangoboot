from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from accounts.views import LogoutView, GroupCreateView, GroupUpdateView, GroupDeleteView


urlpatterns = patterns('',
    url(r'^login',
        TemplateView.as_view(template_name='accounts/login.html'),
        name='login'),
    url(r'^logout',
        LogoutView.as_view(),
        name='logout'),

    url(r'^groups/create',
        GroupCreateView.as_view(),
        name='group_create'),
    url(r'^groups/(?P<slug>[-a-zA-Z0-9_]+)/update',
        GroupUpdateView.as_view(),
        name='group_update'),
    url(r'^groups/(?P<slug>[-a-zA-Z0-9_]+)/delete',
        GroupDeleteView.as_view(),
        name='group_delete'),
)