# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-10 07:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0029_auto_20171005_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter_name',
            name='Filter_Subcategory_Type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ecommapp.SubCategory'),
            preserve_default=False,
        ),
    ]