# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-05 07:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0028_auto_20171002_0716'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Whole_Order_Status',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to='ecommapp.Order_Status_Model'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='TaxOnProduct',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to='ecommapp.Tax'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='couponcode',
            name='Sales_Member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommapp.Sales_Team'),
        ),
    ]