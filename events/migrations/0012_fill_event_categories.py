# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-29 15:56
from __future__ import unicode_literals
import random
from django.db import migrations, models


def update_event_models(apps, schema_editor):
    Category = apps.get_model('events', 'Category')
    Event = apps.get_model('events', 'Event')
    PhysicalEvent = apps.get_model('events', 'PhysicalEvent')
    OnlineEvent = apps.get_model('events', 'OnlineEvent')

    events = Event.objects.all()
    for event in events:
        if event.categories.filter(category_type='P').exists():
            updated_event = PhysicalEvent(event_ptr_id=event.pk, location='')
        else:
            updated_event = OnlineEvent(event_ptr_id=event.pk, url='')
        updated_event.__dict__.update(event.__dict__)
        updated_event.save()


def rollback_event_categories(apps, schema_editor):
    Category = apps.get_model('events', 'Category')

    for category in Category.objects.all():
        category.category_type = random.choice(['O', 'P'])
        category.save()


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0011_auto_20181029_1056'),
    ]

    operations = [
        migrations.RunPython(update_event_models, reverse_code=rollback_event_categories),
    ]
