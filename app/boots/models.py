from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

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

    team = models.ForeignKey(Team, verbose_name=_('owner'))
    slug = SlugField(_('slug'))
    tagline = models.CharField(max_length=250, help_text=_('Short description.'))
    url = models.URLField(_('URL'), null=True, blank=True, help_text=_('Public site or repository.'))
    type = models.CharField(_('type'), max_length=1, choices=TYPES, help_text=_('Type of template.'))
    tags = TaggableManager(verbose_name=_('tags'))

    r_star_count = models.IntegerField(null=True, blank=True)
    r_star_count_daily = models.IntegerField(null=True, blank=True)
    r_star_count_weekly = models.IntegerField(null=True, blank=True)
    r_star_count_monthly = models.IntegerField(null=True, blank=True)

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
    def star_count_daily(self):
        if self.r_star_count_daily is None:
            self.update_star_count()
        return self.r_star_count_daily

    @property
    def star_count_weekly(self):
        if self.r_star_count_weekly is None:
            self.update_star_count()
        return self.r_star_count_weekly

    @property
    def star_count_monthly(self):
        if self.r_star_count_monthly is None:
            self.update_star_count()
        return self.r_star_count_monthly

    def star_count_increment(self, value=1):
        self.r_star_count = self.star_count + value
        self.r_star_count_daily = self.star_count_daily + value
        self.r_star_count_weekly = self.star_count_weekly + value
        self.r_star_count_monthly = self.star_count_monthly + value
        self.save()
        return self.star_count

    def star_count_decrement(self):
        return self.star_count_increment(-1)

    def update_star_count(self):
        self.r_star_count = self.stars.count()
        #TODO: calculate daily, ...
        self.r_star_count_daily = self.stars.count()
        self.r_star_count_weekly = self.stars.count()
        self.r_star_count_monthly = self.stars.count()
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
        ordering = ('-created',)
        get_latest_by = 'created'


@receiver(post_save, sender=Star)
def star_count_increment(sender, instance, created, **kwargs):
    instance.boot.star_count_increment()


@receiver(pre_delete, sender=Star)
def star_count_decrement(sender, instance, **kwargs):
    instance.boot.star_count_decrement()
