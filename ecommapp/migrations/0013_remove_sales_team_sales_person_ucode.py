# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-11 08:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0012_couponcode_tax'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sales_team',
            name='Sales_Person_UCode',
        ),
    ]