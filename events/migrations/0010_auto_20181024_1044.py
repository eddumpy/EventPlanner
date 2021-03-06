# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-24 10:44
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


def update_category_types(apps, schema_editor):
    Category = apps.get_model('events', 'Category')
    for category in Category.objects.all():
        if category.category_type == 'Physical':
            category.category_type = 'P'
        elif category.category_type == 'Online':
            category.category_type = 'O'
        category.save()


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0009_auto_20181023_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_type',
            field=models.CharField(max_length=50, choices=[('P', 'Physical'), ('O', 'Online')]),
        ),
        migrations.RunPython(update_category_types, reverse_code=migrations.RunPython.noop)
    ]
