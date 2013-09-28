# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Group'
        db.create_table(u'accounts_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'accounts', ['Group'])

        # Adding model 'User'
        db.create_table(u'accounts_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='default_users', to=orm['accounts.Group'])),
        ))
        db.send_create_signal(u'accounts', ['User'])

        # Adding M2M table for field groups on 'User'
        m2m_table_name = db.shorten_name(u'accounts_user_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'accounts.user'], null=False)),
            ('group', models.ForeignKey(orm[u'accounts.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'group_id'])


    def backwards(self, orm):
        # Deleting model 'Group'
        db.delete_table(u'accounts_group')

        # Deleting model 'User'
        db.delete_table(u'accounts_user')

        # Removing M2M table for field groups on 'User'
        db.delete_table(db.shorten_name(u'accounts_user_groups'))


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
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'default_users'", 'to': u"orm['accounts.Group']"}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users'", 'symmetrical': 'False', 'to': u"orm['accounts.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['accounts']