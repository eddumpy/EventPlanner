# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-29 16:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0012_fill_event_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='category_type',
        ),
    ]