# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-21 07:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_squashed_0025_auto_20161019_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='agenda',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Agenda'),
        ),
    ]
