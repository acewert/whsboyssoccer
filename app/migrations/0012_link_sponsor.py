# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-27 23:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20171218_2133'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('level', models.IntegerField(choices=[(1, 'Iron'), (2, 'Bronze'), (3, 'Silver'), (4, 'Gold'), (5, 'Platinum')])),
            ],
        ),
    ]
