# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-18 06:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mastery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mastery_type', models.PositiveIntegerField(choices=[(0, 'School'), (1, 'Domain'), (2, 'Bloodline'), (3, 'Mystery'), (4, 'Patron')])),
                ('name', models.CharField(max_length=128)),
                ('specializes', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='spells.Mastery')),
            ],
        ),
        migrations.CreateModel(
            name='MasteryLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.PositiveIntegerField()),
                ('mastery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spells.Mastery')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('must_prepare_spells', models.BooleanField(default=True)),
                ('masteries', models.ManyToManyField(to='spells.Mastery')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerClassLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.PositiveIntegerField()),
                ('player_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spells.PlayerClass')),
            ],
        ),
        migrations.CreateModel(
            name='Spell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('masteries', models.ManyToManyField(through='spells.MasteryLevel', to='spells.Mastery')),
            ],
        ),
        migrations.CreateModel(
            name='SpellsKnown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.PositiveIntegerField()),
                ('mastery_type', models.PositiveIntegerField(default=0)),
                ('num_of_spells', models.PositiveIntegerField()),
                ('apply_attribute_bonus', models.BooleanField(default=True)),
                ('player_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spells.PlayerClass')),
            ],
        ),
        migrations.CreateModel(
            name='SpellsPerDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.PositiveIntegerField()),
                ('mastery_type', models.PositiveIntegerField(default=0)),
                ('num_of_spells', models.PositiveIntegerField()),
                ('apply_attribute_bonus', models.BooleanField(default=True)),
                ('player_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spells.PlayerClass')),
            ],
        ),
        migrations.AddField(
            model_name='playerclasslevel',
            name='spell',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spells.Spell'),
        ),
        migrations.AddField(
            model_name='masterylevel',
            name='spell',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spells.Spell'),
        ),
        migrations.AlterUniqueTogether(
            name='spellsperday',
            unique_together=set([('level', 'player_class', 'mastery_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='spellsknown',
            unique_together=set([('level', 'player_class', 'mastery_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='masterylevel',
            unique_together=set([('level', 'spell', 'mastery')]),
        ),
        migrations.AlterUniqueTogether(
            name='mastery',
            unique_together=set([('mastery_type', 'name')]),
        ),
    ]
