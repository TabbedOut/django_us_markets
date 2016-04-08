# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_us_markets', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='community',
            options={'verbose_name_plural': 'communities'},
        ),
    ]
