# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-08 05:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0003_auto_20170906_1325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='Product_Code',
        ),
        migrations.AlterField(
            model_name='customer',
            name='User_Profile_Pic',
            field=models.ImageField(null=True, upload_to='UserProfilePic/'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='Sub_Category_Slug_Field',
            field=models.SlugField(blank=True, max_length=120),
        ),
    ]
