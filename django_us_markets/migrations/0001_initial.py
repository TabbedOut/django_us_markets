# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostalCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('postal_code', models.CharField(unique=True, max_length=7)),
                ('state', models.SlugField(max_length=255)),
                ('country', models.SlugField(help_text=b'ISO 3166-1 alpha-2', max_length=2)),
                ('center', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('tabulation', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('community', models.ForeignKey(related_name='postal_codes', blank=True, to='django_us_markets.Community', null=True)),
                ('market', models.ForeignKey(related_name='postal_codes', blank=True, to='django_us_markets.Market', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
