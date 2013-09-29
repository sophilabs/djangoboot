from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from accounts.views import LogoutView, TeamCreateView, TeamUpdateView, TeamAddUserView, TeamLeaveView, \
    TeamDeleteView, UserDetailsView


urlpatterns = patterns('',
    url(r'^login',
        TemplateView.as_view(template_name='accounts/login.html'),
        name='login'),
    url(r'^logout',
        LogoutView.as_view(),
        name='logout'),
    url(r'^(?P<team>[-a-zA-Z0-9_\.]+)/details',
        UserDetailsView.as_view(),
        name='user_details'),

    url(r'^teams/create',
        TeamCreateView.as_view(),
        name='team_create'),
    url(r'^teams/(?P<team>[-a-zA-Z0-9_\.]+)/modify',
        TeamUpdateView.as_view(),
        name='team_update'),
    url(r'^teams/(?P<team>[-a-zA-Z0-9_\.]+)/add',
        TeamAddUserView.as_view(),
        name='team_add_user'),
    url(r'^teams/(?P<team>[-a-zA-Z0-9_\.]+)/leave',
        TeamLeaveView.as_view(),
        name='team_leave'),
    url(r'^teams/(?P<team>[-a-zA-Z0-9_\.]+)/delete',
        TeamDeleteView.as_view(),
        name='team_delete'),
)