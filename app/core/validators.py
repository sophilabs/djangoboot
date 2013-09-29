import re

from django.conf import settings
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


slug_re = re.compile(r'^[-a-zA-Z0-9_\.]+$')
validate_slug = validators.RegexValidator(
    slug_re, _("Enter a valid slug consisting of letters, numbers, underscores, hyphens or dots."), 'invalid')


def validate_non_reserved(slug):
    if slug in settings.RESERVED_SLUGS:
        raise ValidationError(_('You cannot use a reserved name as slug.'))
