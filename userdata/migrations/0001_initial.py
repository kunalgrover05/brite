# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-07 12:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataFieldValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('char_val', models.CharField(blank=True, max_length=190, null=True)),
                ('date_val', models.DateField(blank=True, null=True)),
                ('number_val', models.IntegerField(blank=True, null=True)),
                ('enum_val', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.EnumChoice')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.DataField')),
            ],
        ),
        migrations.CreateModel(
            name='UserInsuranceFormDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insurance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.InsuranceForm')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='datafieldvalue',
            name='userInsuranceFormDetail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dataFieldValues', to='userdata.UserInsuranceFormDetail'),
        ),
    ]
