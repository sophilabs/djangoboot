from django.db import models
from django.utils.translation import ugettext as _

from taggit.managers import TaggableManager

from core.models import TimeStampedMixin
from accounts.models import Group


class Boot(TimeStampedMixin, models.Model):
    TYPE_PROJECT = 'P'
    TYPE_APP = 'A'

    TYPES = (
        (TYPE_PROJECT, _('Project')),
        (TYPE_APP, _('Application')),
    )

    group = models.ForeignKey(Group)
    slug = models.SlugField()
    type = models.CharField(max_length=1, choices=TYPES)
    tags = TaggableManager()


class BootVersion(TimeStampedMixin, models.Model):
    boot = models.ForeignKey(Boot)
    source = models.URLField()
    name = models.CharField(max_length=50)
