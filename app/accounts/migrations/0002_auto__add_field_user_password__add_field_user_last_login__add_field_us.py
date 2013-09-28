# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'User.password'
        db.add_column(u'accounts_user', 'password',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128),
                      keep_default=False)

        # Adding field 'User.last_login'
        db.add_column(u'accounts_user', 'last_login',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'User.username'
        db.add_column(u'accounts_user', 'username',
                      self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=100),
                      keep_default=False)

        # Adding field 'User.email'
        db.add_column(u'accounts_user', 'email',
                      self.gf('django.db.models.fields.EmailField')(default='', max_length=75),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'User.password'
        db.delete_column(u'accounts_user', 'password')

        # Deleting field 'User.last_login'
        db.delete_column(u'accounts_user', 'last_login')

        # Deleting field 'User.username'
        db.delete_column(u'accounts_user', 'username')

        # Deleting field 'User.email'
        db.delete_column(u'accounts_user', 'email')


    models = {
        u'accounts.group': {
            'Meta': {'object_name': 'Group'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'accounts.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'default_users'", 'to': u"orm['accounts.Group']"}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users'", 'symmetrical': 'False', 'to': u"orm['accounts.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['accounts']