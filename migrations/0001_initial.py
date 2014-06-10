# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Community'
        db.create_table(u'places_community', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'places', ['Community'])

        # Adding model 'Market'
        db.create_table(u'places_market', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'places', ['Market'])

        # Adding model 'ZIPCode'
        db.create_table(u'places_zipcode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django_localflavor_us.models.USStateField')(max_length=2)),
            ('market', self.gf('django.db.models.fields.related.ForeignKey')(related_name='zip_codes', null=True, to=orm['places.Market'])),
            ('community', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='zip_codes', null=True, to=orm['places.Community'])),
        ))
        db.send_create_signal(u'places', ['ZIPCode'])
        db.execute('ALTER TABLE places_zipcode ENGINE=MyISAM;')

    def backwards(self, orm):
        # Deleting model 'Community'
        db.delete_table(u'places_community')

        # Deleting model 'Market'
        db.delete_table(u'places_market')

        # Deleting model 'ZIPCode'
        db.delete_table(u'places_zipcode')


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
            'community': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'zip_codes'", 'null': 'True', 'to': u"orm['places.Community']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'zip_codes'", 'null': 'True', 'to': u"orm['places.Market']"}),
            'state': ('django_localflavor_us.models.USStateField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['places']
