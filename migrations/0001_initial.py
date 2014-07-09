# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Community'
        db.create_table(u'places_community', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'places', ['Community'])

        # Adding model 'Market'
        db.create_table(u'places_market', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'places', ['Market'])

        # Adding model 'PostalCode'
        db.create_table(u'places_postalcode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=7)),
            ('state', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('country', self.gf('django.db.models.fields.SlugField')(max_length=2)),
            ('market', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='zip_codes', null=True, to=orm['places.Market'])),
            ('community', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='zip_codes', null=True, to=orm['places.Community'])),
        ))
        db.send_create_signal(u'places', ['PostalCode'])
        db.execute('ALTER TABLE places_postalcode ENGINE=MyISAM;')


    def backwards(self, orm):
        # Deleting model 'Community'
        db.delete_table(u'places_community')

        # Deleting model 'Market'
        db.delete_table(u'places_market')

        # Deleting model 'PostalCode'
        db.delete_table(u'places_postalcode')


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
            'community': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'zip_codes'", 'null': 'True', 'to': u"orm['places.Community']"}),
            'country': ('django.db.models.fields.SlugField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'zip_codes'", 'null': 'True', 'to': u"orm['places.Market']"}),
            'postal_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '7'}),
            'state': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['places']
