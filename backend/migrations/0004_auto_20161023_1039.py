# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-23 10:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20161022_1743'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AlterUniqueTogether(
            name='session',
            unique_together=set([]),
        ),
    ]
