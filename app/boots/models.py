from django.db import models
from django.utils.translation import ugettext as _

from taggit.managers import TaggableManager

from core.models import TimeStampedMixin
from accounts.models import Team


class Boot(TimeStampedMixin, models.Model):
    TYPE_PROJECT = 'P'
    TYPE_APP = 'A'

    TYPES = (
        (TYPE_PROJECT, _('project')),
        (TYPE_APP, _('application')),
    )

    team = models.ForeignKey(Team, verbose_name=_('team'))
    slug = models.SlugField(_('slug'))
    tagline = models.CharField(max_length=250)
    url = models.URLField(null=True, blank=True)
    type = models.CharField(_('type'), max_length=1, choices=TYPES)
    tags = TaggableManager(verbose_name=_('tags'))

    class Meta:
        unique_together = (('team', 'slug',),)


class BootVersion(TimeStampedMixin, models.Model):
    boot = models.ForeignKey(Boot, verbose_name=_('boot'))
    slug = models.SlugField(_('slug'))
    source = models.URLField(_('source'))

    @property
    def team(self):
        return self.boot.team

    class Meta:
        unique_together = (('boot', 'slug',),)
