from django.core.urlresolvers import reverse
from django import template


register = template.Library()


def _get_next(context):
    request = context.get('request')
    return request.GET.get('next') or request.get_full_path() if request else None


@register.simple_tag(takes_context=True)
def social(context, backend):
    return reverse('social:begin', args=(backend,)) + '?next=' + _get_next(context)


@register.simple_tag(takes_context=True)
def logout(context):
    return reverse('accounts:logout') + '?next=' + _get_next(context)
