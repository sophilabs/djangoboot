import re

from django.core import validators
from django.utils.translation import ugettext as _


slug_re = re.compile(r'^[-a-zA-Z0-9_\.]+$')
validate_slug = validators.RegexValidator(
    slug_re, _("Enter a valid slug consisting of letters, numbers, underscores, hyphens or dots."), 'invalid')
