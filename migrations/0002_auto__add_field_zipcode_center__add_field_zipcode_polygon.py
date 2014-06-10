# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ZIPCode.center'
        db.add_column(u'places_zipcode', 'center',
                      self.gf('django.contrib.gis.db.models.fields.PointField')(default=None),
                      keep_default=False)

        # Adding field 'ZIPCode.polygon'
        db.add_column(u'places_zipcode', 'tabulation',
                      self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(default=None),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ZIPCode.center'
        db.delete_column(u'places_zipcode', 'center')

        # Deleting field 'ZIPCode.tabulation'
        db.delete_column(u'places_zipcode', 'tabulation')


    models = {
        u'places.community': {
            'Meta': {'object_name': 'Community'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'places.market': {
            'Meta': {'object_name': 'Market'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'places.zipcode': {
            'Meta': {'object_name': 'ZIPCode'},
            'center': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'community': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'zip_codes'", 'null': 'True', 'to': u"orm['places.Community']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'zip_codes'", 'to': u"orm['places.Market']"}),
            'tabulation': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'state': ('django_localflavor_us.models.USStateField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['places']
