# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-07 12:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=190)),
                ('type', models.CharField(choices=[('text', 'Text field'), ('number', 'Number Field'), ('date', 'Date Field'), ('enum', 'Enum Field')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='EnumChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=190)),
            ],
        ),
        migrations.CreateModel(
            name='InsuranceForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=190)),
                ('fields', models.ManyToManyField(to='core.DataField')),
            ],
        ),
        migrations.AddField(
            model_name='datafield',
            name='enum_choices',
            field=models.ManyToManyField(blank=True, to='core.EnumChoice'),
        ),
    ]
