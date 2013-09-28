from django.db import models


class Group(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=100)
    email = models.EmailField()


class User(models.Model):
    group = models.ForeignKey(Group, related_name='default_users')
    groups = models.ManyToManyField(Group, related_name='users')
