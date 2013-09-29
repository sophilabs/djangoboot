from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext as _

from core.models import TimeStampedMixin


class Team(models.Model):
    slug = models.SlugField(_('slug'), unique=True)
    name = models.CharField(_('name'), max_length=100)
    email = models.EmailField(_('email'))
    url = models.URLField(_('URL'), null=True, blank=True)

    @models.permalink
    def get_absolute_url(self):
        return 'boots:team', [self.slug]

    def __unicode__(self):
        return self.name


class UserManager(BaseUserManager):

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = UserManager.normalize_email(email)

        team = Team(slug=username, name=username, email=email)
        team.save(using=self._db)

        user = self.model(team=team, username=email, email=email)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username,  email, password):
        email = UserManager.normalize_email(email)
        u = self.create_user(username, email, password)
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(TimeStampedMixin, AbstractBaseUser, PermissionsMixin):

    username = models.CharField(_('username'), max_length=100, unique=True)
    email = models.EmailField(_('email'), unique=True)

    team = models.ForeignKey(Team, related_name='default_users', verbose_name=_('default team'))
    teams = models.ManyToManyField(Team, related_name='users', verbose_name=_('teams'))

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __unicode__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_superuser

    def get_short_name(self):
        return self.username

    def get_absolute_url(self):
        return self.team.get_absolute_url()
