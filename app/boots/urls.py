from django.conf.urls import patterns, url

from boots.views import SearchView, TrendingView, TeamView, BootView, BootVersionView, BootCreateView, \
    BootUpdateView, BootDeleteView, BootVersionCreateView, BootVersionUpdateView, BootVersionDeleteView, \
    BootVersionMoveView, StarBootView


urlpatterns = patterns('',
    url(r'^star_boot$',
        StarBootView.as_view(),
        name='star_boot'),

    url(r'^search$',
        SearchView.as_view(),
        name='search'),
    url(r'^trending$',
        TrendingView.as_view(),
        name='trending'),
    url(r'^add$',
        BootCreateView.as_view(),
        name='boot_create'),

    url(r'^(?P<team>[-a-zA-Z0-9_\.]+)$',
        TeamView.as_view(),
        name='team'),

    url(r'^(?P<team>[-a-zA-Z0-9_\.]+)/(?P<boot>[-a-zA-Z0-9_\.]+)$',
        BootView.as_view(),
        name='boot'),
    url(r'^(?P<team>[-a-zA-Z0-9_\.]+)/(?P<boot>[-a-zA-Z0-9_\.]+)/update$',
        BootUpdateView.as_view(),
        name='boot_update'),
    url(r'^(?P<team>[-a-zA-Z0-9_\.]+)/(?P<boot>[-a-zA-Z0-9_\.]+)/delete$',
        BootDeleteView.as_view(),
        name='boot_delete'),

    url(r'^(?P<team>[-a-zA-Z0-9_\.]+)/(?P<boot>[-a-zA-Z0-9_\.]+)/add$',
        BootVersionCreateView.as_view(),
        name='boot_version_create'),
     url(r'^(?P<team>[-a-zA-Z0-9_\.]+)/(?P<boot>[-a-zA-Z0-9_\.]+)/(?P<version>[-a-zA-Z0-9_\.]+)/update$',
        BootVersionUpdateView.as_view(),
        name='boot_version_update'),
    url(r'^(?P<team>[-a-zA-Z0-9_\.]+)/(?P<boot>[-a-zA-Z0-9_\.]+)/(?P<version>[-a-zA-Z0-9_\.]+)/up$',
        BootVersionMoveView.as_view(up=True, permanent=False),
        name='boot_version_up'),
    url(r'^(?P<team>[-a-zA-Z0-9_\.]+)/(?P<boot>[-a-zA-Z0-9_\.]+)/(?P<version>[-a-zA-Z0-9_\.]+)/down$',
        BootVersionMoveView.as_view(up=False, permanent=False),
        name='boot_version_down'),
    url(r'^(?P<team>[-a-zA-Z0-9_\.]+)/(?P<boot>[-a-zA-Z0-9_\.]+)/(?P<version>[-a-zA-Z0-9_\.]+)/delete$',
        BootVersionDeleteView.as_view(),
        name='boot_version_delete'),
    url(r'^(?P<team>[-a-zA-Z0-9_\.]+)/(?P<boot>[-a-zA-Z0-9_\.]+)/(?P<version>[-a-zA-Z0-9_\.]+)$',
        BootVersionView.as_view(),
        name='boot_version'),
)