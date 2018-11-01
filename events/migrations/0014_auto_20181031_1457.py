# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-31 14:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0013_remove_category_category_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=300)),
                ('city', models.CharField(max_length=50)),
                ('postcode', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterModelOptions(
            name='event',
            options={},
        ),
        migrations.AlterField(
            model_name='physicalevent',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Location'),
        ),
    ]