from django.db import models
from django.utils.translation import ugettext as _

from taggit.managers import TaggableManager

from core.models import TimeStampedMixin
from accounts.models import Team


class Boot(models.Model, TimeStampedMixin):
    TYPE_PROJECT = 'P'
    TYPE_APP = 'A'

    TYPES = (
        (TYPE_PROJECT, _('Project')),
        (TYPE_APP, _('Application')),
    )

    team = models.ForeignKey(Team, verbose_name=_('owner'))
    slug = models.SlugField(_('slug'))
    tagline = models.CharField(max_length=250, help_text=_('Short description.'))
    url = models.URLField(_('URL'), null=True, blank=True, help_text=_('Public site or repository.'))
    type = models.CharField(_('type'), max_length=1, choices=TYPES, help_text=_('Type of template.'))
    tags = TaggableManager(verbose_name=_('tags'))

    @models.permalink
    def get_absolute_url(self):
        return 'boots:boot', [self.team.slug, self.slug]

    class Meta:
        unique_together = (('team', 'slug',),)


class BootVersion(models.Model, TimeStampedMixin):
    boot = models.ForeignKey(Boot, verbose_name=_('boot'))
    slug = models.SlugField(_('slug'))
    source = models.URLField(_('source'))

    @property
    def team(self):
        return self.boot.team

    @models.permalink
    def get_absolute_url(self):
        return 'boots:boot_version', [self.boot.team.slug, self.boot.slug, self.slug]

    class Meta:
        unique_together = (('boot', 'slug',),)
