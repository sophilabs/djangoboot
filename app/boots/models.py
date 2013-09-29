from datetime import timedelta

from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone

from taggit.managers import TaggableManager

from core.models import TimeStampedMixin, SlugField
from accounts.models import User, Team


class Boot(TimeStampedMixin, models.Model):
    TYPE_PROJECT = 'P'
    TYPE_APP = 'A'
    TYPE_COOKIECUTTER = 'C'

    TYPES = (
        (TYPE_PROJECT, _('Project')),
        (TYPE_APP, _('App')),
        (TYPE_COOKIECUTTER, _('CookieCutter')),
    )

    COMMAND = {
        TYPE_PROJECT: 'startproject',
        TYPE_APP: 'startapp'
    }

    team = models.ForeignKey(Team, verbose_name=_('owner'))
    slug = SlugField(_('slug'))
    tagline = models.CharField(max_length=250, help_text=_('Short description.'))
    url = models.URLField(_('URL'), null=True, blank=True, help_text=_('Public site or repository.'))
    type = models.CharField(_('type'), max_length=1, choices=TYPES, help_text=_('Type of template.'))
    tags = TaggableManager(verbose_name=_('tags'))

    r_star_count = models.IntegerField(null=True, blank=True)
    r_star_count_day = models.IntegerField(null=True, blank=True)
    r_star_count_week = models.IntegerField(null=True, blank=True)
    r_star_count_month = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.slug

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

    @property
    def star_count(self):
        if self.r_star_count is None:
            self.update_star_count()
        return self.r_star_count

    @property
    def star_count_day(self):
        if self.r_star_count_day is None:
            self.update_star_count()
        return self.r_star_count_day

    @property
    def star_count_week(self):
        if self.r_star_count_week is None:
            self.update_star_count()
        return self.r_star_count_week

    @property
    def star_count_month(self):
        if self.r_star_count_month is None:
            self.update_star_count()
        return self.r_star_count_month

    def update_star_count(self):
        self.r_star_count = self.stars.count()

        now = timezone.now()
        self.r_star_count_day = self.stars.filter(timestamp__gte=now - timedelta(days=1)).count()
        self.r_star_count_week = self.stars.filter(timestamp__gte=now - timedelta(days=7)).count()
        self.r_star_count_month = self.stars.filter(timestamp__gte=now - timedelta(days=30)).count()

        self.save()

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
    slug = SlugField(_('slug'), help_text=_('Version slug.'))
    source = models.URLField(_('source'), help_text=_('Template source url.'))
    append = models.CharField(_('command arguments'), help_text=_('Extra command arguments for django-admin.py'),
                              null=True, blank=True, max_length=200)

    def __unicode__(self):
        return unicode(self.boot) + ' ' + self.slug

    def get_command(self):
        if self.boot.type == Boot.TYPE_COOKIECUTTER:
            return u'cookiecutter {source}'.format(
                source=self.source
            )
        else:
            return u'./django-admin.py {type} --template={source} {append}'.format(
                type=Boot.COMMAND[self.boot.type],
                source=self.source,
                append=self.append if self.append else ''
            )

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
        ordering = ('-created',)
        get_latest_by = 'created'


@receiver(post_save, sender=Star)
def star_count_increment(sender, instance, created, **kwargs):
    instance.boot.update_star_count()


@receiver(pre_delete, sender=Star)
def star_count_decrement(sender, instance, **kwargs):
    instance.boot.update_star_count()
