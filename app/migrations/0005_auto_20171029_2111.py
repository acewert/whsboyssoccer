# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-29 21:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20171029_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeniorSpotlight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='')),
                ('bio', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='seniorspotlight',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Player'),
        ),
    ]
