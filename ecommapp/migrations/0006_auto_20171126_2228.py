# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-26 16:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0005_auto_20171126_1818'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size_sf', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='Sizes',
            field=models.ManyToManyField(null=True, to='ecommapp.Size'),
        ),
    ]