# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-19 14:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0004_category_add_to_all_events'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='add_to_all_events',
        ),
    ]
