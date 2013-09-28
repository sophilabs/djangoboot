from django.conf.urls import patterns, url
from boots.views import SearchView

urlpatterns = patterns('',
                       url(r'^search$', SearchView.as_view(), name='search'),
                       url(r'^trending$', SearchView.as_view(), name='trending'),
)