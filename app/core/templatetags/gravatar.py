import hashlib
import urllib

from django import template
from django.utils.html import escape

register = template.Library()


@register.simple_tag
def gravatar(email, size=None, rating=None):
    url = 'http://www.gravatar.com/avatar/{hash}?{parameters}'.format(
        hash=hashlib.md5(email).hexdigest(),
        parameters=urllib.urlencode((('r', rating or 'g',), ('s', size or '80',),), doseq=True))
    return escape(url)