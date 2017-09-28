# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-26 16:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0022_auto_20170926_1645'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='Shipment_Authority',
        ),
        migrations.AddField(
            model_name='product',
            name='Shipment_Authority',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ecommapp.Shipment_Orgs'),
            preserve_default=False,
        ),
    ]