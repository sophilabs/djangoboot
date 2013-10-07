from django.db import models
from django.utils.translation import ugettext as _

from core import forms


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class SlugField(models.SlugField):
    def formfield(self, **kwargs):
        defaults = {'form_class': forms.SlugField}
        defaults.update(kwargs)
        return super(SlugField, self).formfield(**defaults)

    def south_field_triple(self):
        return 'django.db.models.CharField', [], {'max_length': '50', 'db_index': 'True'}

