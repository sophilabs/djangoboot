from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from accounts.views import LogoutView, TeamCreateView, TeamUpdateView, TeamDeleteView


urlpatterns = patterns('',
    url(r'^login',
        TemplateView.as_view(template_name='accounts/login.html'),
        name='login'),
    url(r'^logout',
        LogoutView.as_view(),
        name='logout'),

    url(r'^teams/create',
        TeamCreateView.as_view(),
        name='team_create'),
    url(r'^teams/(?P<slug>[-a-zA-Z0-9_\.]+)/update',
        TeamUpdateView.as_view(),
        name='team_update'),
    url(r'^teams/(?P<slug>[-a-zA-Z0-9_\.]+)/delete',
        TeamDeleteView.as_view(),
        name='team_delete'),
)