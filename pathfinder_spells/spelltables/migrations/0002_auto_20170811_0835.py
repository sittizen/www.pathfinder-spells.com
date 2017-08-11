# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-11 08:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spelltables', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='spell',
            name='components',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spell',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spell',
            name='effect',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]
