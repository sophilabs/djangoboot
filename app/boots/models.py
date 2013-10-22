from datetime import timedelta

from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.utils import timezone

from taggit.managers import TaggableManager
from taggit.models import TaggedItem
from markupfield.fields import MarkupField

from core.models import TimeStampedMixin, SlugField
from accounts.models import User, Team


class Boot(TimeStampedMixin, models.Model):
    TYPE_PROJECT = 'P'
    TYPE_APP = 'A'
    TYPE_COOKIECUTTER = 'C'
    TYPE_PACKAGE = 'K'

    TYPES = (
        (TYPE_PROJECT, _('Template Project')),
        (TYPE_APP, _('Template App')),
        (TYPE_COOKIECUTTER, _('CookieCutter')),
        (TYPE_PACKAGE, _('Package'))
    )

    team = models.ForeignKey(Team, verbose_name=_('owner'))
    slug = SlugField(_('slug'), help_text=_('Boot name. e.g: <code>my-boot</code>.'))
    tagline = models.CharField(max_length=250, help_text=_('Short description.'))
    url = models.URLField(_('URL'), null=True, blank=True,
                          help_text=_('Public site or repository. e.g: <code>http://yourproject.com</code>.'))
    type = models.CharField(_('type'), max_length=1, choices=TYPES, help_text=_('Type of template.'))
    tags = TaggableManager(verbose_name=_('tags'),
                           help_text=_('A comma-separated list of tags. e.g: <code>sphinx</code>, <code>puppet</code>, <code>south</code>.'))
    flagged = models.BooleanField(default=False)

    r_star_count = models.IntegerField(null=True, blank=True)
    r_star_count_day = models.IntegerField(null=True, blank=True)
    r_star_count_week = models.IntegerField(null=True, blank=True)
    r_star_count_month = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.slug

    @property
    def sorted_versions(self):
        return self.versions.order_by('order', '-id')

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

    def latest_version(self):
        try:
            return self.sorted_versions[:1].get()
        except BootVersion.DoesNotExist:
            return None

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
    slug = SlugField(_('slug'), help_text=_('Version slug. e.g: <code>1.0</code> or <code>0.1a</code>.'))
    readme = MarkupField(_('readme'), markup_type='markdown', help_text='You can use <code>markdown</code>.', null=True, blank=True)
    command = models.TextField(_('command'), help_text=_('Command to use the template, cookiecutter or install the package'))
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.boot) + ' ' + self.slug

    @property
    def team(self):
        return self.boot.team

    @models.permalink
    def get_absolute_url(self):
        return 'boots:boot_version', [self.boot.team.slug, self.boot.slug, self.slug]

    @models.permalink
    def get_update_url(self):
        return 'boots:boot_version_update', [self.boot.team.slug, self.boot.slug, self.slug]

    @models.permalink
    def get_delete_url(self):
        return 'boots:boot_version_delete', [self.boot.team.slug, self.boot.slug, self.slug]

    @models.permalink
    def get_up_url(self):
        return 'boots:boot_version_up', [self.boot.team.slug, self.boot.slug, self.slug]

    @models.permalink
    def get_down_url(self):
        return 'boots:boot_version_down', [self.boot.team.slug, self.boot.slug, self.slug]

    class Meta:
        unique_together = (('boot', 'slug',),)
        ordering = ('-created',)


@receiver(post_save, sender=Star)
def star_count_increment(sender, instance, created, **kwargs):
    try:
        instance.boot.update_star_count()
    except:
        pass


@receiver(post_delete, sender=Star)
def star_count_decrement(sender, instance, **kwargs):
    try:
        instance.boot.update_star_count()
    except:
        pass


@receiver(post_save, sender=TaggedItem)
def update_search(sender, instance, **kwargs):
    from haystack import connections
    connections['default'].get_unified_index().get_index(Boot).update_object(instance.content_object)
