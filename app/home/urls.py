from django.conf.urls import patterns
from home.views import IndexView

urlpatterns = patterns('',
                       (r'^$', IndexView.as_view()),
                       )