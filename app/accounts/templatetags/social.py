from django.core.urlresolvers import reverse
from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def social(context, backend):
    request = context.get('request')
    return reverse('social:begin', args=(backend,)) + '?next=' + (request.GET.get('next') or request.get_full_path())
