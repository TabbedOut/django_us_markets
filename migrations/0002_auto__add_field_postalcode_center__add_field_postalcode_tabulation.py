# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PostalCode.center'
        db.add_column(u'places_postalcode', 'center',
                      self.gf('django.contrib.gis.db.models.fields.PointField')(default=None),
                      keep_default=False)

        # Adding field 'PostalCode.tabulation'
        db.add_column(u'places_postalcode', 'tabulation',
                      self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(default=None),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PostalCode.center'
        db.delete_column(u'places_postalcode', 'center')

        # Deleting field 'PostalCode.tabulation'
        db.delete_column(u'places_postalcode', 'tabulation')


    models = {
        u'places.community': {
            'Meta': {'object_name': 'Community'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'places.market': {
            'Meta': {'object_name': 'Market'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'places.postalcode': {
            'Meta': {'object_name': 'PostalCode'},
            'center': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'community': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'zip_codes'", 'null': 'True', 'to': u"orm['places.Community']"}),
            'country': ('django.db.models.fields.SlugField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'zip_codes'", 'null': 'True', 'to': u"orm['places.Market']"}),
            'postal_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '7'}),
            'state': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'tabulation': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {})
        }
    }

    complete_apps = ['places']