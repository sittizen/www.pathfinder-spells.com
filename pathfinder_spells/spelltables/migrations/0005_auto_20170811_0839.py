# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-11 08:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spelltables', '0004_auto_20170811_0839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spell',
            name='effect',
            field=models.CharField(max_length=256, null=True),
        ),
    ]