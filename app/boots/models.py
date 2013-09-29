from django.db import models
from django.utils.translation import ugettext as _

from taggit.managers import TaggableManager

from core.models import TimeStampedMixin
from accounts.models import User, Team


class Boot(TimeStampedMixin, models.Model):
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

    @models.permalink
    def get_update_url(self):
        return 'boots:boot_update', [self.team.slug, self.slug]

    @models.permalink
    def get_delete_url(self):
        return 'boots:boot_delete', [self.team.slug, self.slug]

    @models.permalink
    def get_create_url(self):
        return 'boots:boot_version_create', [self.team.slug, self.slug]

    class Meta:
        unique_together = (('team', 'slug',),)


class Star(models.Model):
    boot = models.ForeignKey(Boot, related_name='stars')
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('boot', 'user',),)


class BootVersion(TimeStampedMixin, models.Model):
    boot = models.ForeignKey(Boot, verbose_name=_('boot'), related_name='versions')
    slug = models.SlugField(_('slug'), help_text=_('Version slug.'))
    source = models.URLField(_('source'), help_text=_('ZIP source containing the template.'))

    @property
    def team(self):
        return self.boot.team

    @models.permalink
    def get_absolute_url(self):
        return 'boots:boot_version', [self.boot.team.slug, self.boot.slug, self.slug]

    @models.permalink
    def get_delete_url(self):
        return 'boots:boot_version_delete', [self.boot.team.slug, self.boot.slug, self.slug]

    class Meta:
        unique_together = (('boot', 'slug',),)
