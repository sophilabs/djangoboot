from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import ugettext as _


class Group(models.Model):
    slug = models.SlugField(_('slug'))
    name = models.CharField(_('name'), max_length=100)
    email = models.EmailField(_('email'))


class User(AbstractBaseUser):
    group = models.ForeignKey(Group, related_name='default_users', verbose_name=_('default group'))
    groups = models.ManyToManyField(Group, related_name='users', verbose_name=_('groups'))

    username = models.CharField(_('username'), max_length=100, unique=True)
    email = models.EmailField(_('email'))


    USERNAME_FIELD = 'username'