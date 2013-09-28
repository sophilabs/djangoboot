from django.conf.urls import patterns, url
from boots.views import SearchView, TrendingView, GroupView, BootView, VersionView

urlpatterns = patterns('',
    url(r'^search$', SearchView.as_view(), name='search'),
    url(r'^trending$', TrendingView.as_view(), name='trending'),
    url(r'^(?P<group>[-a-zA-Z0-9_]+)$', GroupView.as_view(), name='group'),
    url(r'^(?P<group>[-a-zA-Z0-9_]+)/(?P<boot>[-a-zA-Z0-9_]+)$', BootView.as_view(), name='boot'),
    url(r'^(?P<group>[-a-zA-Z0-9_]+)/(?P<boot>[-a-zA-Z0-9_]+)/(?P<version>[-a-zA-Z0-9_]+)$', VersionView.as_view(), name='version'),
)