# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-08 16:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20171207_0609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='squad',
            field=models.IntegerField(choices=[(4, b'Freshman Red'), (1, b'Freshman'), (2, b'JV'), (3, b'Varsity')]),
        ),
    ]
