# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-11 05:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0011_auto_20170910_1215'),
    ]

    operations = [
        migrations.CreateModel(
            name='CouponCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Code', models.TextField(max_length=100)),
                ('Sales_Member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommapp.Sales_Team')),
            ],
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tax_Percentage', models.FloatField()),
                ('Prducts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommapp.SubCategory')),
            ],
        ),
    ]