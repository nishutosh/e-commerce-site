# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-30 16:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0025_auto_20170928_0653'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='Price',
            new_name='Base_Price',
        ),
        migrations.AddField(
            model_name='product',
            name='Discount',
            field=models.FloatField(default=0),
        ),
    ]
