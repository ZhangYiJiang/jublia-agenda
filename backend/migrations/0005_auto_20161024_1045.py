# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-24 10:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20161023_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenda',
            name='duration',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='duration',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
