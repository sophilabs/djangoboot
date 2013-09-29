from django.views.generic import TemplateView
from haystack.query import SearchQuerySet
from boots.models import Boot


class IndexView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        sqs = SearchQuerySet().models(Boot).order_by('-star_count_month')
        kwargs['trending'] = {
            'projects': sqs.filter(type_exact=Boot.TYPE_PROJECT),
            'apps': sqs.filter(type_exact=Boot.TYPE_APP),
            'cookiecutters': sqs.filter(type_exact=Boot.TYPE_COOKIECUTTER),
        }
        return super(IndexView, self).get_context_data(**kwargs)
