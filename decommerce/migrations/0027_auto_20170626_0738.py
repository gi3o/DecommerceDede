# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-26 07:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('decommerce', '0026_remove_product_tech_sheet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='decommerce.UserProfile'),
        ),
        migrations.AlterField(
            model_name='sellerreview',
            name='by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='decommerce.UserProfile'),
        ),
    ]