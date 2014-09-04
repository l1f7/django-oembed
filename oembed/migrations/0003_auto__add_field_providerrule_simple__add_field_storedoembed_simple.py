# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ProviderRule.simple'
        db.add_column(u'oembed_providerrule', 'simple',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'StoredOEmbed.simple'
        db.add_column(u'oembed_storedoembed', 'simple',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ProviderRule.simple'
        db.delete_column(u'oembed_providerrule', 'simple')

        # Deleting field 'StoredOEmbed.simple'
        db.delete_column(u'oembed_storedoembed', 'simple')


    models = {
        u'oembed.providerrule': {
            'Meta': {'object_name': 'ProviderRule'},
            'endpoint': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'format': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'regex': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'simple': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'oembed.storedoembed': {
            'Meta': {'ordering': "('-max_width',)", 'object_name': 'StoredOEmbed'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'html': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json': ('django.db.models.fields.TextField', [], {}),
            'match': ('django.db.models.fields.TextField', [], {}),
            'max_height': ('django.db.models.fields.IntegerField', [], {}),
            'max_width': ('django.db.models.fields.IntegerField', [], {}),
            'simple': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['oembed']