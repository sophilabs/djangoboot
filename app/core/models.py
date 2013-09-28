from django.db import models
from django.utils.translation import ugettext as _


class TimeStampedMixin(object):
    created = models.DateTimeField(_('created'), _auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
