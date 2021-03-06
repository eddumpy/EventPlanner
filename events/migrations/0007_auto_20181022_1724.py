# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-22 17:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0006_auto_20181019_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.CharField(default=b'Online', max_length=50),
        ),
        migrations.AlterField(
            model_name='event',
            name='categories',
            field=models.ManyToManyField(to='events.Category'),
        ),
    ]
