# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-25 06:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0002_auto_20171105_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='Transaction_Id',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]