# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-18 10:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='category',
        ),
        migrations.AddField(
            model_name='event',
            name='category',
            field=models.ManyToManyField(related_name='categories', to='events.Category'),
        ),
    ]
