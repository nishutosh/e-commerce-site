# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-19 07:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0035_seller_seller_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flash_sale_banner',
            name='Flash_Sale_Ancess',
        ),
        migrations.RemoveField(
            model_name='review',
            name='Product',
        ),
        migrations.RemoveField(
            model_name='review',
            name='Reviewer',
        ),
        migrations.RemoveField(
            model_name='flash_sale',
            name='Flash_slug',
        ),
        migrations.RemoveField(
            model_name='shipment_orgs',
            name='Shipping_Company_Id',
        ),
        migrations.AddField(
            model_name='flash_sale',
            name='Flash_Sale_URL',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shipment_orgs',
            name='Shipping_Company_URL',
            field=models.URLField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Flash_Sale_Banner',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]