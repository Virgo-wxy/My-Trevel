# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-04-07 05:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Travel', '0002_auto_20190330_1045'),
    ]

    operations = [
        migrations.CreateModel(
            name='Custom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cf_city', models.CharField(max_length=225)),
                ('dd_city', models.CharField(max_length=225)),
                ('cf_date', models.CharField(max_length=225)),
                ('travel_days', models.IntegerField()),
                ('travel_adult', models.IntegerField()),
                ('travel_children', models.IntegerField()),
                ('name', models.CharField(max_length=225)),
                ('number', models.CharField(max_length=225)),
                ('content', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]