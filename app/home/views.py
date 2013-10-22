from django.views.generic import TemplateView
from django.conf import settings
from haystack.query import SearchQuerySet

from core.views import EnsureCSRFMixin
from boots.models import Boot


class IndexView(EnsureCSRFMixin, TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        sqs = SearchQuerySet().models(Boot).filter(star_count__gt=settings.HOME_TRENDING_STAR, flagged=False). \
            order_by('-star_count_week', '-star_count_month', '-star_count')
        kwargs['trending'] = {
            'templates': sqs.filter(type_exact__in=[Boot.TYPE_PROJECT, Boot.TYPE_APP])[:settings.HOME_TRENDING_COUNT],
            'cookiecutters': sqs.filter(type_exact=Boot.TYPE_COOKIECUTTER)[:settings.HOME_TRENDING_COUNT],
            'packages': sqs.filter(type_exact=Boot.TYPE_PACKAGE)[:settings.HOME_TRENDING_COUNT]
        }
        return super(IndexView, self).get_context_data(**kwargs)
