# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-10 10:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0007_remove_pics_is_detail_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Product_Quantity', models.IntegerField(default=1)),
            ],
        ),
        migrations.RemoveField(
            model_name='cartproduct',
            name='Cart_Product_Belongs_To',
        ),
        migrations.RemoveField(
            model_name='cartproduct',
            name='Product_In_Cart',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='Cart_Id',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='customer',
        ),
        migrations.AddField(
            model_name='cart',
            name='checkout_date',
            field=models.DateField(default=None),
        ),
        migrations.AddField(
            model_name='cart',
            name='date_of_creation',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='CartProduct',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='Cart_Product_Belongs_To',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommapp.Cart'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='Product_In_Cart',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ecommapp.Product'),
        ),
    ]