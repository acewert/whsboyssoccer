# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-16 22:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20180116_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='imgur_token_type',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]