# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-03-30 02:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Travel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartinfo',
            name='travel_number',
            field=models.CharField(max_length=255),
        ),
    ]
