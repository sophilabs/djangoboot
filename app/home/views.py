from django.views.generic import TemplateView
from haystack.query import SearchQuerySet
from boots.models import Boot


class IndexView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        sqs = SearchQuerySet().models(Boot).filter(star_count__gt=5). \
            order_by('-star_count_week', '-star_count_month', '-star_count')
        kwargs['trending'] = {
            'projects': sqs.filter(type_exact=Boot.TYPE_PROJECT)[:5],
            'apps': sqs.filter(type_exact=Boot.TYPE_APP)[:5],
            'cookiecutters': sqs.filter(type_exact=Boot.TYPE_COOKIECUTTER)[:5],
        }
        return super(IndexView, self).get_context_data(**kwargs)
