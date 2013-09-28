from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext as _

from core.models import TimeStampedMixin


class Group(models.Model):
    slug = models.SlugField(_('slug'), unique=True)
    name = models.CharField(_('name'), max_length=100)
    email = models.EmailField(_('email'))


class UserManager(BaseUserManager):

    def create_user(self, username, email=None, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = UserManager.normalize_email(email)

        group = Group(slug=username, name=username, email=email)
        group.save(using=self._db)

        user = self.model(group=group, username=username, email=email)
        user.save(using=self._db)

        return user

    def create_superuser(self):
        pass


class User(TimeStampedMixin, AbstractBaseUser):
    group = models.ForeignKey(Group, related_name='default_users', verbose_name=_('default group'))
    groups = models.ManyToManyField(Group, related_name='users', verbose_name=_('groups'))

    username = models.CharField(_('username'), max_length=100, unique=True)
    email = models.EmailField(_('email'))

    USERNAME_FIELD = 'username'

    objects = UserManager()