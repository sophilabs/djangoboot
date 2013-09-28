# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'BootVersion.name'
        db.delete_column(u'boots_bootversion', 'name')

        # Adding field 'BootVersion.slug'
        db.add_column(u'boots_bootversion', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default='', max_length=50),
                      keep_default=False)

        # Adding unique constraint on 'BootVersion', fields ['boot', 'slug']
        db.create_unique(u'boots_bootversion', ['boot_id', 'slug'])

        # Adding unique constraint on 'Boot', fields ['group', 'slug']
        db.create_unique(u'boots_boot', ['group_id', 'slug'])


    def backwards(self, orm):
        # Removing unique constraint on 'Boot', fields ['group', 'slug']
        db.delete_unique(u'boots_boot', ['group_id', 'slug'])

        # Removing unique constraint on 'BootVersion', fields ['boot', 'slug']
        db.delete_unique(u'boots_bootversion', ['boot_id', 'slug'])

        # Adding field 'BootVersion.name'
        db.add_column(u'boots_bootversion', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)

        # Deleting field 'BootVersion.slug'
        db.delete_column(u'boots_bootversion', 'slug')


    models = {
        u'accounts.group': {
            'Meta': {'object_name': 'Group'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'boots.boot': {
            'Meta': {'unique_together': "(('group', 'slug'),)", 'object_name': 'Boot'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
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