# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-25 14:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0002_cart_credits_used'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Order_Price_Raw',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='Order_Total_Price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='coupon_code_used_in_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommapp.CouponCode'),
        ),
        migrations.AddField(
            model_name='order',
            name='credits_used_in_order',
            field=models.IntegerField(default=0),
        ),
    ]