# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Boot'
        db.create_table(u'boots_boot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Team'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('tagline', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'boots', ['Boot'])

        # Adding unique constraint on 'Boot', fields ['team', 'slug']
        db.create_unique(u'boots_boot', ['team_id', 'slug'])

        # Adding model 'BootVersion'
        db.create_table(u'boots_bootversion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('boot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['boots.Boot'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('source', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'boots', ['BootVersion'])

        # Adding unique constraint on 'BootVersion', fields ['boot', 'slug']
        db.create_unique(u'boots_bootversion', ['boot_id', 'slug'])


    def backwards(self, orm):
        # Removing unique constraint on 'BootVersion', fields ['boot', 'slug']
        db.delete_unique(u'boots_bootversion', ['boot_id', 'slug'])

        # Removing unique constraint on 'Boot', fields ['team', 'slug']
        db.delete_unique(u'boots_boot', ['team_id', 'slug'])

        # Deleting model 'Boot'
        db.delete_table(u'boots_boot')

        # Deleting model 'BootVersion'
        db.delete_table(u'boots_bootversion')


    models = {
        u'accounts.team': {
            'Meta': {'object_name': 'Team'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'boots.boot': {
            'Meta': {'unique_together': "(('team', 'slug'),)", 'object_name': 'Boot'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Team']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'boots.bootversion': {
            'Meta': {'unique_together': "(('boot', 'slug'),)", 'object_name': 'BootVersion'},
            'boot': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['boots.Boot']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'source': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['boots']